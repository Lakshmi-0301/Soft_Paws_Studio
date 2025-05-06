document.getElementById('paymentForm').addEventListener('submit', function(event) {
    let firstName = document.getElementById('first_name').value.trim();
    let apartment = document.getElementById('apartment_number').value.trim();
    let street = document.getElementById('street_name').value.trim();
    let city = document.getElementById('city').value.trim();
    let state = document.getElementById('state').value.trim();
    let country = document.getElementById('country').value.trim();
    let pincode = document.getElementById('pincode').value.trim();
    let paymentMode = document.querySelector('input[name="payment_mode"]:checked');

    if (!firstName || !apartment || !street || !city || !state || !country || !pincode || !paymentMode) {
        alert('Please fill all required fields.');
        event.preventDefault();
    }
});
