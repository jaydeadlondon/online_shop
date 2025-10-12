// Wishlist functionality
function addToWishlist(productId, productName) {
    if (!document.body.dataset.userAuthenticated) {
        window.location.href = '/login/?next=' + window.location.pathname;
        return;
    }
    
    fetch('/api/wishlist/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(`${productName} added to wishlist!`);
        } else {
            showNotification('Error adding to wishlist', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error adding to wishlist', 'error');
    });
}

function addToCart(productId, productName, quantity = 1) {
    if (!document.body.dataset.userAuthenticated) {
        window.location.href = '/login/?next=' + window.location.pathname;
        return;
    }
    
    fetch('/api/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ 
            product_id: productId,
            quantity: quantity 
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(`${productName} added to cart!`);
            updateCartCount(data.cart_count);
        } else {
            showNotification('Error adding to cart', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error adding to cart', 'error');
    });
}

function updateCartCount(count) {
    const cartCountElements = document.querySelectorAll('.cart-count');
    cartCountElements.forEach(el => {
        el.textContent = count;
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

