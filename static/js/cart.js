// Cart functionality
document.addEventListener('alpine:init', () => {
    Alpine.data('cart', () => ({
        items: [],
        isOpen: false,
        loading: false,

        init() {
            this.loadCart();
        },

        async loadCart() {
            try {
                const response = await fetch('/api/cart/');
                if (response.ok) {
                    const data = await response.json();
                    this.items = data.items || [];
                }
            } catch (error) {
                console.error('Error loading cart:', error);
            }
        },

        async addToCart(productId, quantity = 1) {
            this.loading = true;
            try {
                const response = await fetch('/api/cart/add_item/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCookie('csrftoken'),
                    },
                    body: JSON.stringify({
                        product_id: productId,
                        quantity: quantity,
                    }),
                });

                if (response.ok) {
                    await this.loadCart();
                    this.isOpen = true;
                    this.showNotification('Product added to cart!');
                }
            } catch (error) {
                console.error('Error adding to cart:', error);
                this.showNotification('Error adding product to cart', 'error');
            } finally {
                this.loading = false;
            }
        },

        async removeFromCart(itemId) {
            try {
                const response = await fetch(`/api/cart/remove_item/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCookie('csrftoken'),
                    },
                    body: JSON.stringify({ item_id: itemId }),
                });

                if (response.ok) {
                    await this.loadCart();
                }
            } catch (error) {
                console.error('Error removing from cart:', error);
            }
        },

        get total() {
            return this.items.reduce((sum, item) => {
                return sum + (parseFloat(item.product.price) * item.quantity);
            }, 0).toFixed(2);
        },

        get itemCount() {
            return this.items.reduce((sum, item) => sum + item.quantity, 0);
        },

        getCookie(name) {
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
        },

        showNotification(message, type = 'success') {
            // Simple notification (can be enhanced with a toast library)
            const notification = document.createElement('div');
            notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg text-white z-50 ${
                type === 'error' ? 'bg-red-500' : 'bg-green-500'
            }`;
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
        },
    }));
});

