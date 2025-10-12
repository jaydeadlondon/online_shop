from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Brand, Category, Season, Size, Product
from .serializers import (
    BrandSerializer, CategorySerializer, SeasonSerializer, 
    SizeSerializer, ProductListSerializer, ProductDetailSerializer
)


def products_list(request):
    """Список товаров"""
    products = Product.objects.filter(is_available=True).select_related(
        'brand', 'category', 'season', 'size'
    ).prefetch_related('images')
    
    search_query = request.GET.get('search', '').strip()
    brand_id = request.GET.get('brand')
    category_id = request.GET.get('category')
    condition = request.GET.get('condition')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    ordering = request.GET.get('ordering', '-created_at')
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(brand__name__icontains=search_query)
        )
    
    if brand_id:
        products = products.filter(brand_id=brand_id)
    if category_id:
        products = products.filter(category_id=category_id)
    if condition:
        products = products.filter(condition=condition)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    products = products.order_by(ordering)
    
    brands = Brand.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')
    
    context = {
        'products': products,
        'brands': brands,
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    """Детальная страница товара"""
    product = get_object_or_404(
        Product.objects.select_related('brand', 'category', 'season', 'size')
        .prefetch_related('images'),
        slug=slug,
        is_available=True
    )
    
    if product.size:
        available_sizes = Size.objects.filter(category=product.size.category).order_by('value')
    else:
        available_sizes = Size.objects.filter(category='clothing').order_by('value')
    
    context = {
        'product': product,
        'available_sizes': available_sizes,
    }
    return render(request, 'products/product_detail.html', context)


def brands_list(request):
    """Список брендов"""
    brands = Brand.objects.all().order_by('name')
    
    context = {
        'brands': brands,
    }
    return render(request, 'products/brands.html', context)


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для брендов"""
    
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для категорий"""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'


class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для сезонов"""
    
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [permissions.AllowAny]


class SizeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для размеров"""
    
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [permissions.AllowAny]


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для товаров"""
    
    queryset = Product.objects.filter(is_available=True).select_related(
        'brand', 'category', 'season', 'size'
    ).prefetch_related('images')
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['brand', 'category', 'condition', 'is_featured']
    search_fields = ['name', 'description', 'brand__name']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        size = self.request.query_params.get('size')
        if size:
            queryset = queryset.filter(size__value=size)
        
        color = self.request.query_params.get('color')
        if color:
            queryset = queryset.filter(color__icontains=color)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def similar(self, request, slug=None):
        """Получить похожие товары"""
        product = self.get_object()
        similar_products = Product.objects.filter(
            Q(brand=product.brand) | Q(category=product.category),
            is_available=True
        ).exclude(id=product.id)[:6]
        
        serializer = ProductListSerializer(
            similar_products, many=True, context={'request': request}
        )
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Получить избранные товары"""
        featured = self.get_queryset().filter(is_featured=True)[:8]
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)
