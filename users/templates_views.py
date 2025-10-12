from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def login_view(request):
    """Страница входа"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # В нашей модели USERNAME_FIELD = 'email', поэтому authenticate ожидает email
        from users.models import User
        user = None
        
        # Если ввели username, получаем email
        if '@' not in username_or_email:
            try:
                user_obj = User.objects.get(username=username_or_email)
                email = user_obj.email
            except User.DoesNotExist:
                email = username_or_email  # Возможно это email
        else:
            email = username_or_email
        
        # Аутентифицируем по email (т.к. USERNAME_FIELD = 'email')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'users/login.html')


def register_view(request):
    """Страница регистрации"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        from users.models import User
        
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    
    return render(request, 'users/register.html')


def logout_view(request):
    """Выход"""
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    """Профиль пользователя"""
    return render(request, 'users/profile.html')


@login_required
def wishlist_view(request):
    """Wishlist пользователя"""
    wishlist_products = request.user.wishlist.all()
    
    context = {
        'wishlist_products': wishlist_products,
    }
    return render(request, 'users/wishlist.html', context)


def cart_view(request):
    """Корзина"""
    from orders.models import Cart
    from decimal import Decimal
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.select_related('product__brand', 'product__category').prefetch_related('product__images').all()
        
        # Рассчитываем стоимость доставки
        shipping_cost = Decimal('0.00') if cart.total_price >= 200 else Decimal('10.00')
    else:
        cart = None
        cart_items = []
        shipping_cost = Decimal('0.00')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'shipping_cost': shipping_cost,
    }
    return render(request, 'orders/cart.html', context)

