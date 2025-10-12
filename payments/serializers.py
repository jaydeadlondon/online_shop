from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор платежа"""
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'order', 'stripe_payment_intent_id', 'amount', 'currency', 
                 'status', 'status_display', 'payment_method', 'created_at', 'paid_at']
        read_only_fields = ['id', 'stripe_payment_intent_id', 'created_at', 'paid_at']


class PaymentIntentCreateSerializer(serializers.Serializer):
    """Сериализатор для создания Payment Intent"""
    
    order_id = serializers.IntegerField()

