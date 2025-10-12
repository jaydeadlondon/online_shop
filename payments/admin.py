from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['stripe_payment_intent_id', 'order', 'amount', 'currency', 'status', 'created_at', 'paid_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['stripe_payment_intent_id', 'order__order_number']
    readonly_fields = ['stripe_payment_intent_id', 'created_at', 'updated_at', 'paid_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('order', 'stripe_payment_intent_id', 'amount', 'currency', 'status', 'payment_method')
        }),
        ('Метаданные', {
            'fields': ('metadata', 'error_message'),
            'classes': ('collapse',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at', 'paid_at')
        }),
    )
