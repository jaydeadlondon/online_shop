from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import EmailLog


@shared_task
def send_email_task(recipient, subject, message, email_type, user_id=None):
    """Общая задача для отправки email"""
    
    email_log = EmailLog.objects.create(
        recipient=recipient,
        user_id=user_id,
        email_type=email_type,
        subject=subject,
        status='pending'
    )
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )
        
        email_log.status = 'sent'
        email_log.sent_at = timezone.now()
        email_log.save()
        
        return f"Email успешно отправлен на {recipient}"
    
    except Exception as e:
        email_log.status = 'failed'
        email_log.error_message = str(e)
        email_log.save()
        
        return f"Ошибка отправки email на {recipient}: {str(e)}"


@shared_task
def send_order_created_email(order_id):
    """Отправить email о создании заказа"""
    
    from orders.models import Order
    
    try:
        order = Order.objects.get(id=order_id)
        
        subject = f'Заказ #{order.order_number} создан'
        message = f'''
Здравствуйте!

Ваш заказ #{order.order_number} успешно создан.

Сумма заказа: ${order.total_price}
Статус: {order.get_status_display()}

Мы свяжемся с вами в ближайшее время.

С уважением,
Archive Shop
        '''
        
        send_email_task.delay(
            recipient=order.user.email,
            subject=subject,
            message=message,
            email_type='order_created',
            user_id=order.user.id
        )
    
    except Order.DoesNotExist:
        pass


@shared_task
def send_order_paid_email(order_id):
    """Отправить email об оплате заказа"""
    
    from orders.models import Order
    
    try:
        order = Order.objects.get(id=order_id)
        
        subject = f'Заказ #{order.order_number} оплачен'
        message = f'''
Здравствуйте!

Ваш заказ #{order.order_number} успешно оплачен.

Сумма оплаты: ${order.total_price}

Мы приступили к обработке вашего заказа.

С уважением,
Archive Shop
        '''
        
        send_email_task.delay(
            recipient=order.user.email,
            subject=subject,
            message=message,
            email_type='order_paid',
            user_id=order.user.id
        )
    
    except Order.DoesNotExist:
        pass


@shared_task
def send_order_shipped_email(order_id):
    """Отправить email об отправке заказа"""
    
    from orders.models import Order
    
    try:
        order = Order.objects.get(id=order_id)
        
        subject = f'Заказ #{order.order_number} отправлен'
        message = f'''
Здравствуйте!

Ваш заказ #{order.order_number} отправлен.

Трек-номер для отслеживания: {order.tracking_number}

С уважением,
Archive Shop
        '''
        
        send_email_task.delay(
            recipient=order.user.email,
            subject=subject,
            message=message,
            email_type='order_shipped',
            user_id=order.user.id
        )
    
    except Order.DoesNotExist:
        pass


@shared_task
def send_order_delivered_email(order_id):
    """Отправить email о доставке заказа"""
    
    from orders.models import Order
    
    try:
        order = Order.objects.get(id=order_id)
        
        subject = f'Заказ #{order.order_number} доставлен'
        message = f'''
Здравствуйте!

Ваш заказ #{order.order_number} успешно доставлен.

Спасибо за покупку!

С уважением,
Archive Shop
        '''
        
        send_email_task.delay(
            recipient=order.user.email,
            subject=subject,
            message=message,
            email_type='order_delivered',
            user_id=order.user.id
        )
    
    except Order.DoesNotExist:
        pass

