from django.db import models
from django.conf import settings


class EmailLog(models.Model):
    """Лог отправленных email"""
    
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('sent', 'Отправлено'),
        ('failed', 'Ошибка'),
    ]
    
    TYPE_CHOICES = [
        ('registration', 'Регистрация'),
        ('password_reset', 'Восстановление пароля'),
        ('order_created', 'Заказ создан'),
        ('order_paid', 'Заказ оплачен'),
        ('order_shipped', 'Заказ отправлен'),
        ('order_delivered', 'Заказ доставлен'),
        ('newsletter', 'Рассылка'),
    ]
    
    recipient = models.EmailField(verbose_name='Получатель')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                            null=True, blank=True, related_name='email_logs', verbose_name='Пользователь')
    email_type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name='Тип письма')
    subject = models.CharField(max_length=255, verbose_name='Тема')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    error_message = models.TextField(blank=True, verbose_name='Сообщение об ошибке')
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата отправки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Лог Email'
        verbose_name_plural = 'Логи Email'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_email_type_display()} - {self.recipient}"
