from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Address
from .serializers import (
    UserSerializer, UserCreateSerializer, AddressSerializer, WishlistSerializer
)
from products.models import Product

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для пользователей"""
    
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Получить информацию о текущем пользователе"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Обновить профиль текущего пользователя"""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def wishlist(self, request):
        """Получить wishlist пользователя"""
        from products.serializers import ProductListSerializer
        products = request.user.wishlist.all()
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_to_wishlist(self, request):
        """Добавить товар в wishlist"""
        serializer = WishlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            product = Product.objects.get(id=serializer.validated_data['product_id'])
        except Product.DoesNotExist:
            return Response(
                {'error': 'Товар не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        request.user.wishlist.add(product)
        return Response({'message': 'Товар добавлен в wishlist'})
    
    @action(detail=False, methods=['post'])
    def remove_from_wishlist(self, request):
        """Удалить товар из wishlist"""
        serializer = WishlistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            product = Product.objects.get(id=serializer.validated_data['product_id'])
        except Product.DoesNotExist:
            return Response(
                {'error': 'Товар не найден'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        request.user.wishlist.remove(product)
        return Response({'message': 'Товар удален из wishlist'})


class AddressViewSet(viewsets.ModelViewSet):
    """ViewSet для адресов"""
    
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
