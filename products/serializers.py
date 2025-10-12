from rest_framework import serializers
from .models import Brand, Category, Season, Size, Product, ProductImage


class BrandSerializer(serializers.ModelSerializer):
    """Сериализатор бренда"""
    
    class Meta:
        model = Brand
        fields = ['id', 'name', 'description', 'logo', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории"""
    
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'parent', 'parent_name']


class SeasonSerializer(serializers.ModelSerializer):
    """Сериализатор сезона"""
    
    class Meta:
        model = Season
        fields = ['id', 'name', 'season_type', 'year']


class SizeSerializer(serializers.ModelSerializer):
    """Сериализатор размера"""
    
    class Meta:
        model = Size
        fields = ['id', 'category', 'value']


class ProductImageSerializer(serializers.ModelSerializer):
    """Сериализатор изображения товара"""
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'order', 'is_primary']


class ProductListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка товаров"""
    
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'brand_name', 'category_name', 'price', 
                 'condition', 'is_featured', 'is_available', 'slug', 'primary_image']
    
    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            return self.context['request'].build_absolute_uri(primary.image.url)
        first_image = obj.images.first()
        if first_image:
            return self.context['request'].build_absolute_uri(first_image.image.url)
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра товара"""
    
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    season = SeasonSerializer(read_only=True)
    size = SizeSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'brand', 'category', 'season', 
                 'condition', 'size', 'color', 'material', 'price', 'is_featured', 
                 'is_available', 'slug', 'images', 'created_at', 'updated_at']

