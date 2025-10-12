from rest_framework import serializers
from .models import Cart, CartItem, Coupon, Order, OrderItem, OrderStatusHistory
from products.serializers import ProductListSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """Сериализатор элемента корзины"""
    
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'subtotal', 'added_at']
        read_only_fields = ['id', 'added_at']


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор корзины"""
    
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'total_items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CouponSerializer(serializers.ModelSerializer):
    """Сериализатор промокода"""
    
    is_valid = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_type', 'discount_value', 'is_valid']


class CouponValidateSerializer(serializers.Serializer):
    """Сериализатор для проверки промокода"""
    
    code = serializers.CharField()


class OrderItemSerializer(serializers.ModelSerializer):
    """Сериализатор элемента заказа"""
    
    product = ProductListSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'quantity', 'subtotal']


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    """Сериализатор истории статусов"""
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = OrderStatusHistory
        fields = ['id', 'status', 'status_display', 'note', 'changed_at']


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор заказа"""
    
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'status', 'status_display', 'subtotal', 
                 'shipping_cost', 'discount', 'total_price', 'shipping_address', 
                 'billing_address', 'shipping_method', 'payment_method', 
                 'tracking_number', 'items', 'status_history', 'created_at', 
                 'updated_at', 'paid_at']
        read_only_fields = ['id', 'order_number', 'created_at', 'updated_at', 'paid_at']


class OrderCreateSerializer(serializers.Serializer):
    """Сериализатор для создания заказа"""
    
    shipping_address_id = serializers.IntegerField()
    billing_address_id = serializers.IntegerField(required=False, allow_null=True)
    shipping_method = serializers.ChoiceField(choices=Order.SHIPPING_METHOD_CHOICES)
    payment_method = serializers.ChoiceField(choices=Order.PAYMENT_METHOD_CHOICES)
    coupon_code = serializers.CharField(required=False, allow_blank=True)

