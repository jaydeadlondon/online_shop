from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json

from products.models import Product
from orders.models import Cart, CartItem


@require_http_methods(["POST"])
@login_required
def add_to_cart_api(request):
    """API для добавления товара в корзину"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        product = Product.objects.get(id=product_id, is_available=True)
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        cart_count = cart.items.count()
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart',
            'cart_count': cart_count
        })
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@require_http_methods(["POST"])
@login_required
def add_to_wishlist_api(request):
    """API для добавления товара в wishlist"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        product = Product.objects.get(id=product_id, is_available=True)
        
        if request.user.wishlist.filter(id=product_id).exists():
            return JsonResponse({
                'success': True,
                'message': 'Product already in wishlist'
            })
        
        request.user.wishlist.add(product)
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to wishlist'
        })
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@require_http_methods(["POST"])
@login_required
def remove_from_wishlist_api(request):
    """API для удаления товара из wishlist"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        product = Product.objects.get(id=product_id)
        request.user.wishlist.remove(product)
        
        return JsonResponse({
            'success': True,
            'message': 'Product removed from wishlist'
        })
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

