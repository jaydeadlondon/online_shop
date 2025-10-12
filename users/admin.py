from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Address


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'role', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_staff', 'is_superuser', 'newsletter_subscription']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'phone']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'phone', 'avatar')}),
        ('Настройки', {'fields': ('role', 'newsletter_subscription')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'role'),
        }),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'city', 'country', 'is_default', 'created_at']
    list_filter = ['is_default', 'country', 'created_at']
    search_fields = ['full_name', 'user__email', 'city', 'country', 'phone']
    readonly_fields = ['created_at', 'updated_at']