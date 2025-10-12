from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Address

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'phone', 
                 'avatar', 'newsletter_subscription', 'role', 'date_joined']
        read_only_fields = ['id', 'date_joined', 'role']


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm', 
                 'first_name', 'last_name', 'newsletter_subscription']
    
    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError("Пароли не совпадают")
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AddressSerializer(serializers.ModelSerializer):
    """Сериализатор адреса"""
    
    class Meta:
        model = Address
        fields = ['id', 'user', 'full_name', 'phone', 'country', 'city', 
                 'postal_code', 'address_line1', 'address_line2', 'is_default', 
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class WishlistSerializer(serializers.Serializer):
    """Сериализатор для добавления/удаления из wishlist"""
    
    product_id = serializers.IntegerField()

