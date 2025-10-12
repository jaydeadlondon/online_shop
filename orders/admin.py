from django.contrib import admin
from .models import Cart, CartItem, Coupon, Order, OrderItem, OrderStatusHistory


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['added_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price', 'created_at', 'updated_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at', 'total_items', 'total_price']
    inlines = [CartItemInline]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'valid_from', 'valid_to', 'active', 'times_used', 'usage_limit']
    list_filter = ['discount_type', 'active', 'valid_from', 'valid_to']
    search_fields = ['code']
    readonly_fields = ['times_used', 'created_at']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['subtotal']


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ['changed_at', 'changed_by']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total_price', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'shipping_method', 'created_at']
    search_fields = ['order_number', 'user__email', 'tracking_number']
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'paid_at']
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'order_number', 'status', 'created_at', 'updated_at', 'paid_at')
        }),
        ('Цены', {
            'fields': ('subtotal', 'shipping_cost', 'discount', 'total_price', 'coupon')
        }),
        ('Доставка и оплата', {
            'fields': ('shipping_method', 'payment_method', 'tracking_number')
        }),
        ('Адреса', {
            'fields': ('shipping_address', 'billing_address'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_processing', 'mark_as_shipped']
    
    def mark_as_processing(self, request, queryset):
        for order in queryset:
            order.status = 'processing'
            order.save()
            OrderStatusHistory.objects.create(
                order=order,
                status='processing',
                changed_by=request.user,
                note='Изменено через админ-панель'
            )
    mark_as_processing.short_description = "Отметить как 'В обработке'"
    
    def mark_as_shipped(self, request, queryset):
        for order in queryset:
            order.status = 'shipped'
            order.save()
            OrderStatusHistory.objects.create(
                order=order,
                status='shipped',
                changed_by=request.user,
                note='Изменено через админ-панель'
            )
    mark_as_shipped.short_description = "Отметить как 'Отправлен'"
