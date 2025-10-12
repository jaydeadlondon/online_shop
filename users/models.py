from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Расширенная модель пользователя"""
    
    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    ]
    
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    newsletter_subscription = models.BooleanField(default=False, verbose_name='Подписка на рассылку')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer', verbose_name='Роль')
    wishlist = models.ManyToManyField('products.Product', related_name='wishlisted_by', blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email


class Address(models.Model):
    """Модель адреса доставки"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='Пользователь')
    full_name = models.CharField(max_length=100, verbose_name='Полное имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    country = models.CharField(max_length=50, verbose_name='Страна')
    city = models.CharField(max_length=50, verbose_name='Город')
    postal_code = models.CharField(max_length=20, verbose_name='Почтовый индекс')
    address_line1 = models.CharField(max_length=255, verbose_name='Адрес (строка 1)')
    address_line2 = models.CharField(max_length=255, blank=True, verbose_name='Адрес (строка 2)')
    is_default = models.BooleanField(default=False, verbose_name='Адрес по умолчанию')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.country}"
    
    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
