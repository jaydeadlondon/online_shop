import uuid
from django.db import models
from django.conf import settings


class Cart(models.Model):
    """Модель корзины"""
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                                related_name='cart', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
    
    def __str__(self):
        return f"Корзина пользователя {self.user.email}"
    
    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Элемент корзины"""
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    
    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
    @property
    def subtotal(self):
        return self.product.price * self.quantity


class Coupon(models.Model):
    """Модель промокода"""
    
    DISCOUNT_TYPE_CHOICES = [
        ('percentage', 'Процент'),
        ('fixed', 'Фиксированная сумма'),
    ]
    
    code = models.CharField(max_length=50, unique=True, verbose_name='Код')
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES, verbose_name='Тип скидки')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Значение скидки')
    valid_from = models.DateTimeField(verbose_name='Действителен с')
    valid_to = models.DateTimeField(verbose_name='Действителен до')
    active = models.BooleanField(default=True, verbose_name='Активен')
    usage_limit = models.PositiveIntegerField(null=True, blank=True, verbose_name='Лимит использований')
    times_used = models.PositiveIntegerField(default=0, verbose_name='Использован раз')
    
    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
        ordering = ['-created_at']
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return self.code
    
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        if not self.active:
            return False
        if now < self.valid_from or now > self.valid_to:
            return False
        if self.usage_limit and self.times_used >= self.usage_limit:
            return False
        return True


class Order(models.Model):
    """Модель заказа"""
    
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Карта'),
        ('paypal', 'PayPal'),
    ]
    
    SHIPPING_METHOD_CHOICES = [
        ('standard', 'Стандартная доставка'),
        ('express', 'Экспресс доставка'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                            related_name='orders', verbose_name='Пользователь')
    order_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Номер заказа')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    
    # Цены
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма товаров')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Стоимость доставки')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Скидка')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Итоговая сумма')
    
    # Промокод
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, 
                              related_name='orders', verbose_name='Промокод')
    
    # Адреса (хранятся как JSON для истории)
    shipping_address = models.JSONField(verbose_name='Адрес доставки')
    billing_address = models.JSONField(null=True, blank=True, verbose_name='Адрес плательщика')
    
    # Доставка и оплата
    shipping_method = models.CharField(max_length=20, choices=SHIPPING_METHOD_CHOICES, 
                                      default='standard', verbose_name='Способ доставки')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')
    tracking_number = models.CharField(max_length=100, blank=True, verbose_name='Трек-номер')
    
    # Даты
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата оплаты')
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ {self.order_number} - {self.user.email}"


class OrderItem(models.Model):
    """Элемент заказа"""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена на момент покупки')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    
    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
    @property
    def subtotal(self):
        return self.price * self.quantity


class OrderStatusHistory(models.Model):
    """История изменения статуса заказа"""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history', verbose_name='Заказ')
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES, verbose_name='Статус')
    note = models.TextField(blank=True, verbose_name='Примечание')
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                   null=True, blank=True, verbose_name='Изменено пользователем')
    
    class Meta:
        verbose_name = 'История статуса заказа'
        verbose_name_plural = 'История статусов заказов'
        ordering = ['-changed_at']
    
    def __str__(self):
        return f"Заказ {self.order.order_number} - {self.get_status_display()}"
