from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Cart, CartItem, Coupon, Order, OrderItem, OrderStatusHistory
from .serializers import (
    CartSerializer, CartItemSerializer, CouponSerializer, 
    CouponValidateSerializer, OrderSerializer, OrderCreateSerializer
)
from users.models import Address
from products.models import Product


class CartViewSet(viewsets.ViewSet):
    """ViewSet для корзины"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        """Получить корзину пользователя"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Добавить товар в корзину"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product = get_object_or_404(Product, id=serializer.validated_data['product_id'])
        
        if not product.is_available:
            return Response(
                {'error': 'Товар недоступен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': serializer.validated_data.get('quantity', 1)}
        )
        
        if not created:
            cart_item.quantity += serializer.validated_data.get('quantity', 1)
            cart_item.save()
        
        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['patch'])
    def update_item(self, request):
        """Обновить количество товара в корзине"""
        cart = get_object_or_404(Cart, user=request.user)
        item_id = request.data.get('item_id')
        quantity = request.data.get('quantity', 1)
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.quantity = quantity
        cart_item.save()
        
        return Response(CartItemSerializer(cart_item).data)
    
    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        """Удалить товар из корзины"""
        cart = get_object_or_404(Cart, user=request.user)
        item_id = request.data.get('item_id')
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        
        return Response({'message': 'Товар удален из корзины'}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['delete'])
    def clear(self, request):
        """Очистить корзину"""
        cart = get_object_or_404(Cart, user=request.user)
        cart.items.all().delete()
        
        return Response({'message': 'Корзина очищена'}, status=status.HTTP_204_NO_CONTENT)


class CouponViewSet(viewsets.ViewSet):
    """ViewSet для промокодов"""
    
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def validate(self, request):
        """Проверить промокод"""
        serializer = CouponValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            coupon = Coupon.objects.get(code=serializer.validated_data['code'])
        except Coupon.DoesNotExist:
            return Response(
                {'error': 'Промокод не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not coupon.is_valid():
            return Response(
                {'error': 'Промокод недействителен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(CouponSerializer(coupon).data)


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet для заказов"""
    
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            'items__product', 'status_history'
        )
    
    def create(self, request):
        """Создать заказ"""
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cart = get_object_or_404(Cart, user=request.user)
        if not cart.items.exists():
            return Response(
                {'error': 'Корзина пуста'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Получить адреса
        shipping_address = get_object_or_404(
            Address, id=serializer.validated_data['shipping_address_id'], user=request.user
        )
        
        billing_address_id = serializer.validated_data.get('billing_address_id')
        billing_address = None
        if billing_address_id:
            billing_address = get_object_or_404(
                Address, id=billing_address_id, user=request.user
            )
        
        # Рассчитать стоимость
        subtotal = cart.total_price
        shipping_cost = 15.00 if serializer.validated_data['shipping_method'] == 'standard' else 30.00
        discount = 0
        
        # Применить промокод
        coupon = None
        coupon_code = serializer.validated_data.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                if coupon.is_valid():
                    if coupon.discount_type == 'percentage':
                        discount = subtotal * (coupon.discount_value / 100)
                    else:
                        discount = coupon.discount_value
                    coupon.times_used += 1
                    coupon.save()
            except Coupon.DoesNotExist:
                pass
        
        total_price = subtotal + shipping_cost - discount
        
        # Создать заказ
        order = Order.objects.create(
            user=request.user,
            status='pending',
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            discount=discount,
            total_price=total_price,
            coupon=coupon,
            shipping_address={
                'full_name': shipping_address.full_name,
                'phone': shipping_address.phone,
                'country': shipping_address.country,
                'city': shipping_address.city,
                'postal_code': shipping_address.postal_code,
                'address_line1': shipping_address.address_line1,
                'address_line2': shipping_address.address_line2,
            },
            billing_address={
                'full_name': billing_address.full_name,
                'phone': billing_address.phone,
                'country': billing_address.country,
                'city': billing_address.city,
                'postal_code': billing_address.postal_code,
                'address_line1': billing_address.address_line1,
                'address_line2': billing_address.address_line2,
            } if billing_address else None,
            shipping_method=serializer.validated_data['shipping_method'],
            payment_method=serializer.validated_data['payment_method'],
        )
        
        # Создать элементы заказа
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity
            )
        
        # Создать запись в истории статусов
        OrderStatusHistory.objects.create(
            order=order,
            status='pending',
            changed_by=request.user,
            note='Заказ создан'
        )
        
        # Очистить корзину
        cart.items.all().delete()
        
        return Response(
            OrderSerializer(order).data, 
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Отменить заказ"""
        order = self.get_object()
        
        if order.status not in ['pending', 'paid']:
            return Response(
                {'error': 'Заказ нельзя отменить'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = 'cancelled'
        order.save()
        
        OrderStatusHistory.objects.create(
            order=order,
            status='cancelled',
            changed_by=request.user,
            note='Отменено пользователем'
        )
        
        return Response(OrderSerializer(order).data)
