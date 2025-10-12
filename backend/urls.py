from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from backend.views import home
from products.views import products_list, product_detail, brands_list
from users.templates_views import (
    login_view, register_view, logout_view, 
    profile_view, wishlist_view, cart_view
)
from content.templates_views import (
    faq_view, contact_view, about_view,
    shipping_view, returns_view
)
from users.cart_wishlist_api import (
    add_to_cart_api, add_to_wishlist_api, remove_from_wishlist_api
)
from orders.checkout_views import checkout_view
from users.views import UserViewSet, AddressViewSet
from products.views import BrandViewSet, CategoryViewSet, SeasonViewSet, SizeViewSet, ProductViewSet
from orders.views import CartViewSet, CouponViewSet, OrderViewSet
from payments.views import PaymentViewSet, stripe_webhook
from content.views import PageViewSet, BlogPostViewSet, FAQViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'addresses', AddressViewSet, basename='address')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'seasons', SeasonViewSet, basename='season')
router.register(r'sizes', SizeViewSet, basename='size')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'coupons', CouponViewSet, basename='coupon')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'pages', PageViewSet, basename='page')
router.register(r'blog', BlogPostViewSet, basename='blogpost')
router.register(r'faq', FAQViewSet, basename='faq')

urlpatterns = [
    # Django Template Views
    path('', home, name='home'),
    path('products/', products_list, name='products_list'),
    path('products/<slug:slug>/', product_detail, name='product_detail'),
    path('brands/', brands_list, name='brands_list'),
    
    # Auth
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    # User
    path('profile/', profile_view, name='profile'),
    path('wishlist/', wishlist_view, name='wishlist'),
    path('cart/', cart_view, name='cart'),
    path('checkout/', checkout_view, name='checkout'),
    
    # Content
    path('faq/', faq_view, name='faq'),
    path('contact/', contact_view, name='contact'),
    path('about/', about_view, name='about'),
    path('shipping/', shipping_view, name='shipping'),
    path('returns/', returns_view, name='returns'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API
    path('api/', include(router.urls)),
    path('api/auth/', include('allauth.urls')),
    path('api/cart/add/', add_to_cart_api, name='api_add_to_cart'),
    path('api/wishlist/add/', add_to_wishlist_api, name='api_add_to_wishlist'),
    path('api/wishlist/remove/', remove_from_wishlist_api, name='api_remove_from_wishlist'),
    path('api/payments/webhook/stripe/', stripe_webhook, name='stripe-webhook'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
