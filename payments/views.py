import stripe
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Payment
from .serializers import PaymentSerializer, PaymentIntentCreateSerializer
from orders.models import Order, OrderStatusHistory

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для платежей"""
    
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def create_intent(self, request):
        """Создать Payment Intent для Stripe"""
        serializer = PaymentIntentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        order = get_object_or_404(
            Order, 
            id=serializer.validated_data['order_id'], 
            user=request.user
        )
        
        if order.status != 'pending':
            return Response(
                {'error': 'Заказ уже оплачен или отменен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Создать Payment Intent в Stripe
            intent = stripe.PaymentIntent.create(
                amount=int(order.total_price * 100),  # Конвертировать в центы
                currency='usd',
                metadata={
                    'order_id': order.id,
                    'order_number': str(order.order_number)
                }
            )
            
            # Создать запись о платеже
            payment = Payment.objects.create(
                order=order,
                stripe_payment_intent_id=intent.id,
                amount=order.total_price,
                currency='usd',
                status='pending'
            )
            
            return Response({
                'client_secret': intent.client_secret,
                'payment_id': payment.id,
                'publishable_key': settings.STRIPE_PUBLIC_KEY
            })
        
        except stripe.error.StripeError as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def stripe_webhook(request):
    """Webhook для обработки событий Stripe"""
    
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Обработка события payment_intent.succeeded
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        
        try:
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent['id'])
            payment.status = 'succeeded'
            payment.paid_at = timezone.now()
            payment.save()
            
            # Обновить статус заказа
            order = payment.order
            order.status = 'paid'
            order.paid_at = timezone.now()
            order.save()
            
            # Добавить в историю
            OrderStatusHistory.objects.create(
                order=order,
                status='paid',
                note='Оплата успешно обработана'
            )
            
            # Отправить email уведомление (через Celery)
            from notifications.tasks import send_order_paid_email
            send_order_paid_email.delay(order.id)
            
        except Payment.DoesNotExist:
            pass
    
    # Обработка события payment_intent.payment_failed
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        
        try:
            payment = Payment.objects.get(stripe_payment_intent_id=payment_intent['id'])
            payment.status = 'failed'
            payment.error_message = payment_intent.get('last_payment_error', {}).get('message', '')
            payment.save()
        except Payment.DoesNotExist:
            pass
    
    return HttpResponse(status=200)
