from rest_framework import serializers
from .models import Page, BlogPost, FAQ


class PageSerializer(serializers.ModelSerializer):
    """Сериализатор страницы"""
    
    class Meta:
        model = Page
        fields = ['id', 'title', 'slug', 'content', 'meta_description', 'created_at', 'updated_at']


class BlogPostListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка блог-постов"""
    
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'author_name', 'featured_image', 
                 'tags', 'published_at', 'created_at']


class BlogPostDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра блог-поста"""
    
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'slug', 'content', 'author_name', 'featured_image', 
                 'tags', 'published_at', 'created_at', 'updated_at']


class FAQSerializer(serializers.ModelSerializer):
    """Сериализатор FAQ"""
    
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'order']

