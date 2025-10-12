from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Page(models.Model):
    """Модель статической страницы"""
    
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Slug')
    content = models.TextField(verbose_name='Содержание')
    meta_description = models.CharField(max_length=160, blank=True, verbose_name='Meta описание')
    published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
        ordering = ['title']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    """Модель блог-поста"""
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                              related_name='blog_posts', verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Slug')
    content = models.TextField(verbose_name='Содержание')
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name='Изображение')
    tags = models.CharField(max_length=200, blank=True, verbose_name='Теги (через запятую)')
    published = models.BooleanField(default=False, verbose_name='Опубликовано')
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата публикации')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Блог-пост'
        verbose_name_plural = 'Блог-посты'
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        if self.published and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)


class FAQ(models.Model):
    """Модель часто задаваемых вопросов"""
    
    question = models.CharField(max_length=255, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.question
