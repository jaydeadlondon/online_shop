// Main JavaScript functionality

// Smooth scroll behavior
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scroll to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Image lazy loading fallback for older browsers
    if ('loading' in HTMLImageElement.prototype) {
        const images = document.querySelectorAll('img[loading="lazy"]');
        images.forEach(img => {
            img.src = img.dataset.src || img.src;
        });
    } else {
        // Fallback for browsers that don't support lazy loading
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/lazysizes/5.3.2/lazysizes.min.js';
        document.body.appendChild(script);
    }
});

// Add animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all elements with class 'observe-animation'
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.observe-animation').forEach(el => {
        observer.observe(el);
    });
});

// Add to cart functionality
function addToCart(productId, productName) {
    // This will be used by Alpine.js cart component
    if (window.Alpine && window.Alpine.store('cart')) {
        window.Alpine.store('cart').addToCart(productId);
    } else {
        console.log(`Adding product ${productId} (${productName}) to cart`);
        showNotification(`${productName} added to cart!`);
    }
}

// Simple notification system
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `fixed top-20 right-4 px-6 py-3 rounded-lg text-white z-50 shadow-lg transform transition-all duration-300 ${
        type === 'error' ? 'bg-red-500' : 
        type === 'warning' ? 'bg-yellow-500' : 
        'bg-green-500'
    }`;
    notification.style.transform = 'translateX(400px)';
    notification.innerHTML = `
        <div class="flex items-center gap-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                ${type === 'error' ? 
                    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>' :
                    '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>'
                }
            </svg>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Form validation helper
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Newsletter subscription
function subscribeNewsletter(form) {
    const email = form.querySelector('input[type="email"]').value;
    
    if (!validateEmail(email)) {
        showNotification('Please enter a valid email address', 'error');
        return false;
    }
    
    // Here you would make an AJAX request to your backend
    showNotification('Thank you for subscribing!');
    form.reset();
    return false;
}

// Price formatting
function formatPrice(price) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(price);
}

// Initialize tooltips (if needed)
document.addEventListener('DOMContentLoaded', function() {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'absolute bg-gray-900 text-white text-xs rounded py-1 px-2 z-50';
            tooltip.textContent = this.getAttribute('data-tooltip');
            tooltip.style.bottom = '100%';
            tooltip.style.left = '50%';
            tooltip.style.transform = 'translateX(-50%)';
            tooltip.style.marginBottom = '5px';
            this.style.position = 'relative';
            this.appendChild(tooltip);
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltip = this.querySelector('.absolute');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });
});

