from django.db import models
from django.conf import settings


class Payment(models.Model):
    """Модель платежа"""
    
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('processing', 'В обработке'),
        ('succeeded', 'Успешно'),
        ('failed', 'Ошибка'),
        ('cancelled', 'Отменен'),
        ('refunded', 'Возвращен'),
    ]
    
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, 
                             related_name='payments', verbose_name='Заказ')
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True, 
                                                verbose_name='Stripe Payment Intent ID')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    currency = models.CharField(max_length=3, default='USD', verbose_name='Валюта')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    payment_method = models.CharField(max_length=50, blank=True, verbose_name='Способ оплаты')
    
    # Метаданные
    metadata = models.JSONField(null=True, blank=True, verbose_name='Метаданные')
    error_message = models.TextField(blank=True, verbose_name='Сообщение об ошибке')
    
    # Даты
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата оплаты')
    
    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Платеж {self.stripe_payment_intent_id} - {self.amount} {self.currency}"
