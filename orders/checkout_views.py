from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from decimal import Decimal
import stripe
import json

from orders.models import Cart, Order
from users.models import Address

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout_view(request):
    """Страница оформления заказа"""
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.select_related('product__brand', 'product__category').prefetch_related('product__images').all()
        
        if not cart_items:
            return redirect('cart')
        
        # Рассчитываем стоимость
        subtotal = cart.total_price
        shipping_cost = Decimal('0.00') if subtotal >= 200 else Decimal('10.00')
        total = subtotal + shipping_cost
        
        if request.method == 'POST':
            # Обработка платежа через Stripe
            payment_method_id = request.POST.get('payment_method_id')
            
            if not payment_method_id:
                return JsonResponse({'error': 'Payment method is required'}, status=400)
            
            try:
                # Создаем PaymentIntent
                intent = stripe.PaymentIntent.create(
                    amount=int(total * 100),  # Stripe использует центы
                    currency='usd',
                    payment_method=payment_method_id,
                    confirm=True,
                    automatic_payment_methods={
                        'enabled': True,
                        'allow_redirects': 'never'
                    },
                    metadata={
                        'user_id': request.user.id,
                        'user_email': request.user.email,
                    }
                )
                
                if intent.status == 'requires_action':
                    # Требуется 3D Secure
                    return JsonResponse({
                        'requires_action': True,
                        'payment_intent_client_secret': intent.client_secret,
                        'redirect_url': '/order-success/'  # URL успешного заказа
                    })
                elif intent.status == 'succeeded':
                    # Платеж успешен, создаем заказ
                    order = create_order_from_cart(
                        cart=cart,
                        user=request.user,
                        shipping_cost=shipping_cost,
                        payment_intent_id=intent.id,
                        shipping_info={
                            'first_name': request.POST.get('first_name'),
                            'last_name': request.POST.get('last_name'),
                            'email': request.POST.get('email'),
                            'address': request.POST.get('address'),
                            'city': request.POST.get('city'),
                            'state': request.POST.get('state'),
                            'zip_code': request.POST.get('zip_code'),
                            'country': request.POST.get('country'),
                        }
                    )
                    
                    # Очищаем корзину
                    cart.items.all().delete()
                    
                    return JsonResponse({
                        'success': True,
                        'redirect_url': f'/orders/{order.id}/'
                    })
                else:
                    return JsonResponse({'error': 'Payment failed'}, status=400)
                    
            except stripe.error.CardError as e:
                return JsonResponse({'error': str(e.user_message)}, status=400)
            except Exception as e:
                return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)
        
        context = {
            'cart': cart,
            'cart_items': cart_items,
            'subtotal': subtotal,
            'shipping_cost': shipping_cost,
            'total': total,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        }
        return render(request, 'orders/checkout.html', context)
        
    except Cart.DoesNotExist:
        return redirect('cart')


def create_order_from_cart(cart, user, shipping_cost, payment_intent_id, shipping_info):
    """Создает заказ из корзины"""
    # Создаем или получаем адрес доставки
    address, created = Address.objects.get_or_create(
        user=user,
        address_line1=shipping_info['address'],
        city=shipping_info['city'],
        state=shipping_info['state'],
        postal_code=shipping_info['zip_code'],
        country=shipping_info['country'],
        defaults={
            'address_type': 'shipping',
            'is_default': False,
        }
    )
    
    # Создаем заказ
    order = Order.objects.create(
        user=user,
        shipping_address=address,
        billing_address=address,
        subtotal=cart.total_price,
        shipping_cost=shipping_cost,
        total=cart.total_price + shipping_cost,
        status='pending',
    )
    
    # Копируем товары из корзины в заказ
    from orders.models import OrderItem
    for cart_item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price,
        )
    
    # Создаем запись о платеже
    from payments.models import Payment
    Payment.objects.create(
        order=order,
        amount=order.total,
        payment_method='stripe',
        status='completed',
        transaction_id=payment_intent_id,
    )
    
    return order

