function decreaseQuantity() {
    let displayQty = document.getElementById("display-quantity");
    let hiddenQty = document.getElementById("quantity-input");
    let value = parseInt(displayQty.value);

    if (value > 1) {
        displayQty.value = value - 1;
        hiddenQty.value = displayQty.value;
    }
}

function increaseQuantity() {
    let displayQty = document.getElementById("display-quantity");
    let hiddenQty = document.getElementById("quantity-input");
    let value = parseInt(displayQty.value);
    let maxStock = parseInt(displayQty.getAttribute("data-max")) || 99;

    if (value < maxStock) {
        displayQty.value = value + 1;
        hiddenQty.value = displayQty.value;
    }
}

document.getElementById("cart-form").addEventListener("submit", function(event) {
    let hiddenQty = document.getElementById("quantity-input");
    let displayQty = document.getElementById("display-quantity");

    // Ensure the correct quantity is sent in the form
    hiddenQty.value = displayQty.value;
});
