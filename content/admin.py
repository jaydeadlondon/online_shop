from django.contrib import admin
from .models import Page, BlogPost, FAQ


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'published', 'created_at', 'updated_at']
    list_filter = ['published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published', 'published_at', 'created_at']
    list_filter = ['published', 'published_at', 'created_at']
    search_fields = ['title', 'content', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('author', 'title', 'slug', 'content', 'featured_image')
        }),
        ('Метаданные', {
            'fields': ('tags', 'published', 'published_at')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'active', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['question', 'answer']
    readonly_fields = ['created_at', 'updated_at']
