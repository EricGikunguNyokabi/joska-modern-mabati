document.querySelectorAll('.add-to-cart-form').forEach(form => {
    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the form from submitting normally

        const productId = this.dataset.productId;

        // Use fetch to send a POST request to the cart route
        fetch("{{ url_for('cart.cart_content') }}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                product_id: productId  // Send the product_id as JSON
            })
        })
        .then(response => response.json())
        .then(data => {
            // Optionally update the UI, e.g., show a notification or update cart counter
            console.log(data.message || "Product added to cart!");
        })
        .catch(error => console.error('Error:', error));
    });
});