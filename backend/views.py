from django.shortcuts import render
from products.models import Product


def home(request):
    """Главная страница"""
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:4]
    
    context = {
        'featured_products': featured_products,
    }
    return render(request, 'home.html', context)

