// Cart management – stored in localStorage
window.getCart = function() {
    const stored = localStorage.getItem('novaCart');
    return stored ? JSON.parse(stored) : [];
};

window.saveCart = function(cart) {
    localStorage.setItem('novaCart', JSON.stringify(cart));
    window.dispatchEvent(new Event('cartUpdated'));
};

window.addToCart = function(productId) {
    const cart = window.getCart();
    const existing = cart.find(item => item.id === productId);
    if (existing) {
        existing.qty += 1;
    } else {
        cart.push({ id: productId, qty: 1 });
    }
    window.saveCart(cart);
};

window.removeFromCart = function(productId) {
    let cart = window.getCart();
    cart = cart.filter(item => item.id !== productId);
    window.saveCart(cart);
};

window.updateCartItem = function(productId, delta) {
    const cart = window.getCart();
    const item = cart.find(i => i.id === productId);
    if (item) {
        const newQty = item.qty + delta;
        if (newQty <= 0) {
            window.removeFromCart(productId);
        } else {
            item.qty = newQty;
            window.saveCart(cart);
        }
    }
};

window.clearCart = function() {
    window.saveCart([]);
};

window.getCartCount = function() {
    const cart = window.getCart();
    return cart.reduce((sum, item) => sum + item.qty, 0);
};

window.updateCartBadge = function() {
    const badge = document.getElementById('cartCount');
    if (badge) {
        const count = window.getCartCount();
        badge.textContent = count;
        badge.style.display = count > 0 ? 'inline-block' : 'none';
    }
};

// Auto‑update badge on cart events
window.addEventListener('cartUpdated', window.updateCartBadge);
