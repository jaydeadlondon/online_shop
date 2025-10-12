from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Brand, Category, Season, Size, Product, ProductImage


@admin.register(Brand)
class BrandAdmin(ImportExportModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug', 'created_at']
    list_filter = ['parent']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['name', 'season_type', 'year']
    list_filter = ['season_type', 'year']
    search_fields = ['name']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['category', 'value']
    list_filter = ['category']
    search_fields = ['value']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'order', 'is_primary']


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = ['name', 'brand', 'category', 'price', 'condition', 'is_available', 'is_featured', 'created_at']
    list_filter = ['brand', 'category', 'condition', 'is_available', 'is_featured', 'created_at']
    search_fields = ['name', 'description', 'brand__name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProductImageInline]
    
    actions = ['make_featured', 'make_unavailable', 'make_available']
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    make_featured.short_description = "Отметить как избранное"
    
    def make_unavailable(self, request, queryset):
        queryset.update(is_available=False)
    make_unavailable.short_description = "Сделать недоступным"
    
    def make_available(self, request, queryset):
        queryset.update(is_available=True)
    make_available.short_description = "Сделать доступным"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'order', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name']
