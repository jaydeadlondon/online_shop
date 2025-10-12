from django.shortcuts import render, get_object_or_404
from .models import Page, BlogPost, FAQ


def faq_view(request):
    """FAQ страница"""
    faqs = FAQ.objects.filter(active=True).order_by('order')
    
    context = {
        'faqs': faqs,
    }
    return render(request, 'content/faq.html', context)


def contact_view(request):
    """Контакты"""
    return render(request, 'content/contact.html')


def about_view(request):
    """О нас"""
    return render(request, 'content/about.html')


def blog_view(request):
    """Блог"""
    posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    
    context = {
        'posts': posts,
    }
    return render(request, 'content/blog.html', context)


def shipping_view(request):
    """Доставка"""
    return render(request, 'content/shipping.html')


def returns_view(request):
    """Возвраты"""
    return render(request, 'content/returns.html')

