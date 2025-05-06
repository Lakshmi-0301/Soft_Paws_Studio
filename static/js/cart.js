async function fetchCart() {
    try {
        let response = await fetch("/accounts/cart/data");
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

        let data = await response.json();
        console.log("Cart Data:", data);

        updateCart(data.cart_items);
        updateCartTotals(data.cart_total, data.sales_tax, data.grand_total);
    } catch (error) {
        console.error("Error fetching cart data:", error);
        document.getElementById("cart-items-container").innerHTML = 
            "<tr><td colspan='5'>Failed to load cart.</td></tr>";
    }
}

function updateCart(cartItems) {
    let cartContainer = document.getElementById("cart-items-container");

    if (!cartItems || cartItems.length === 0) {
        cartContainer.innerHTML = "<tr><td colspan='5'>Your cart is empty.</td></tr>";
        return;
    }

    cartContainer.innerHTML = cartItems.map(item => `
        <tr>
            <td>
                <img src="${item.image}" alt="${item.product_name}" width="50">
                ${item.product_name}
            </td>
            <td>$${item.price.toFixed(2)}</td>
            <td>
                <form onsubmit="return false;">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${getCSRFToken()}">
                    <button class="qty-btn" onclick="changeQty(${item.id}, 'decrease', event)"
                        ${item.quantity <= 1 ? 'disabled' : ''}>-</button>
                    <span>${item.quantity}</span>
                    <button class="qty-btn" onclick="changeQty(${item.id}, 'increase', event)"
                        ${item.quantity >= item.stock ? 'disabled' : ''}>+</button>
                </form>
            </td>
            <td>$${(item.price * item.quantity).toFixed(2)}</td>
            <td>
                <button onclick="removeFromCart(${item.id})">Remove</button>
            </td>
        </tr>
    `).join('');

    document.querySelectorAll('.qty-btn[disabled]').forEach(btn => {
        btn.style.opacity = '0.5';
        btn.style.cursor = 'not-allowed';
    });
}

function updateCartTotals(cartTotal, salesTax, grandTotal) {
    document.getElementById("cart-total").innerText = `$${cartTotal.toFixed(2)}`;
    document.getElementById("sales-tax").innerText = `$${salesTax.toFixed(2)}`;
    document.getElementById("shipping-fee").innerText = cartTotal < 100 ? "$5.00" : "$0.00";
    document.getElementById("grand-total").innerText = `$${grandTotal.toFixed(2)}`;
}

function changeQty(itemId, action, event) {
    const button = event.target;
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fa fa-spinner fa-spin"></i>';
    button.disabled = true;

    fetch(`/accounts/cart/update/${itemId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken()
        },
        body: `action=${action}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.cart_items) {
            updateCart(data.cart_items);
            updateCartTotals(data.cart_total, data.sales_tax, data.grand_total);
        }
    })
    .catch(error => {
        console.error("Error updating quantity:", error);
    })
    .finally(() => {
        button.innerHTML = originalText;
    });
}

async function removeFromCart(productId) {
    try {
        let response = await fetch(`/accounts/cart/remove/${productId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
        });

        let data = await response.json();
        if (data.success) {
            fetchCart();
        }
    } catch (error) {
        console.error("Error removing item:", error);
    }
}

function getCSRFToken() {
    let cookies = document.cookie.split("; ");
    for (let cookie of cookies) {
        let [name, value] = cookie.split("=");
        if (name === "csrftoken") {
            return value;
        }
    }
    return "";
}

document.addEventListener('DOMContentLoaded', fetchCart);
