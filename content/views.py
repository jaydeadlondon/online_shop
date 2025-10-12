from rest_framework import viewsets, permissions
from .models import Page, BlogPost, FAQ
from .serializers import (
    PageSerializer, BlogPostListSerializer, 
    BlogPostDetailSerializer, FAQSerializer
)


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для статических страниц"""
    
    queryset = Page.objects.filter(published=True)
    serializer_class = PageSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для блог-постов"""
    
    queryset = BlogPost.objects.filter(published=True).select_related('author')
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        return BlogPostListSerializer


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для FAQ"""
    
    queryset = FAQ.objects.filter(active=True)
    serializer_class = FAQSerializer
    permission_classes = [permissions.AllowAny]
