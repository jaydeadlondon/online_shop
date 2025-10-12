from django.db import models
from django.utils.text import slugify


class Brand(models.Model):
    """Модель бренда"""
    
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    logo = models.ImageField(upload_to='brands/', blank=True, null=True, verbose_name='Логотип')
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name='Slug')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    """Модель категории с поддержкой вложенности"""
    
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name='Slug')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                               related_name='children', verbose_name='Родительская категория')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Season(models.Model):
    """Модель сезона коллекции"""
    
    SEASON_CHOICES = [
        ('SS', 'Spring/Summer'),
        ('FW', 'Fall/Winter'),
    ]
    
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    season_type = models.CharField(max_length=2, choices=SEASON_CHOICES, verbose_name='Тип сезона')
    year = models.IntegerField(verbose_name='Год')
    
    class Meta:
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'
        ordering = ['-year', 'season_type']
    
    def __str__(self):
        return self.name


class Size(models.Model):
    """Справочник размеров"""
    
    CATEGORY_CHOICES = [
        ('clothing', 'Одежда'),
        ('shoes', 'Обувь'),
        ('accessories', 'Аксессуары'),
    ]
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Категория')
    value = models.CharField(max_length=10, verbose_name='Значение')
    
    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        unique_together = ['category', 'value']
        ordering = ['category', 'value']
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.value}"


class Product(models.Model):
    """Модель товара"""
    
    CONDITION_CHOICES = [
        ('new', 'Новое'),
        ('excellent', 'Отличное'),
        ('good', 'Хорошее'),
        ('fair', 'Удовлетворительное'),
    ]
    
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', verbose_name='Бренд')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True, blank=True, 
                               related_name='products', verbose_name='Сезон')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good', verbose_name='Состояние')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, 
                            related_name='products', verbose_name='Размер')
    color = models.CharField(max_length=50, blank=True, verbose_name='Цвет')
    material = models.CharField(max_length=100, blank=True, verbose_name='Материал')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    is_featured = models.BooleanField(default=False, verbose_name='Избранное')
    is_available = models.BooleanField(default=True, verbose_name='В наличии')
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name='Slug')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['brand', 'category']),
            models.Index(fields=['is_available', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.brand.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.brand.name} {self.name}")
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    """Модель изображений товара"""
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_primary = models.BooleanField(default=False, verbose_name='Главное изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Изображение для {self.product.name}"
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)
