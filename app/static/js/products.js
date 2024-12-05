document.addEventListener('DOMContentLoaded', function() {
    var cartItems = document.querySelectorAll('.cart-row');

    // Function to update total price for a row
    function updateTotal(row) {
        var priceElement = row.querySelector('.cart-price');
        var quantityElement = row.querySelector('.cart-quantity-input');
        var totalElement = row.querySelector('.cart-total');
        var price = parseFloat(priceElement.innerText.replace('KSh. ', '').replace(',', ''));
        var quantity = parseInt(quantityElement.value);
        if (isNaN(quantity) || quantity < 1) {
            quantity = 1;
            quantityElement.value = 1;
        }
        var total = price * quantity;
        totalElement.innerText = 'KSh. ' + total.toFixed(2);
    }

    // Function to update the overall cart total
    function updateCartTotal() {
        var cartRows = document.querySelectorAll('.cart-row');
        var total = 0;
        cartRows.forEach(function(row) {
            var totalElement = row.querySelector('.cart-total');
            var totalPrice = parseFloat(totalElement.innerText.replace('KSh. ', '').replace(',', ''));
            total += totalPrice;
        });
        document.querySelector('.cart-total-price').innerText = 'KSh. ' + total.toFixed(2);
    }

    // Initial calculation of total prices for all cart items
    cartItems.forEach(function(item) {
        updateTotal(item);
    });
    updateCartTotal();

    // Event listener for quantity changes
    cartItems.forEach(function(item) {
        var quantityInput = item.querySelector('.cart-quantity-input');
        quantityInput.addEventListener('change', function() {
            updateTotal(item);
            updateCartTotal();
        });
    });

    // Event listener for remove buttons
    var removeButtons = document.querySelectorAll('.btn-danger');
    removeButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            var row = event.target.closest('.cart-row');
            row.remove();
            updateCartTotal();
        });
    });

    // Event listener for clear cart button
    document.querySelector('.btn-clear').addEventListener('click', function() {
        var cartItemsContainer = document.querySelector('.cart-items');
        while (cartItemsContainer.firstChild) {
            cartItemsContainer.removeChild(cartItemsContainer.firstChild);
        }
        updateCartTotal();
    });

    // Event listener for purchase button
    document.querySelector('.btn-purchase').addEventListener('click', function() {
        var cartItemsContainer = document.querySelector('.cart-items');
        var cartRows = cartItemsContainer.querySelectorAll('.cart-row');
        var cartData = [];
        cartRows.forEach(function(row) {
            var name = row.querySelector('.cart-item-title').innerText;
            var price = parseFloat(row.querySelector('.cart-price').innerText.replace('KSh. ', '').replace(',', ''));
            var quantity = parseInt(row.querySelector('.cart-quantity-input').value);
            var total = parseFloat(row.querySelector('.cart-total').innerText.replace('KSh. ', '').replace(',', ''));
            cartData.push({ name: name, price: price, quantity: quantity, total: total });
        });

        // Send cartData to server for processing (you can use fetch or Axios for this)
        fetch('/purchase', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(cartData),
        })
            .then(function(response) {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(function(data) {
                // Optionally handle response data here
                console.log(data);
                // Clear cart after successful purchase
                while (cartItemsContainer.firstChild) {
                    cartItemsContainer.removeChild(cartItemsContainer.firstChild);
                }
                updateCartTotal();
                alert('Thank you for your purchase!');
            })
            .catch(function(error) {
                console.error('There has been a problem with your fetch operation:', error);
            });
    });
});
