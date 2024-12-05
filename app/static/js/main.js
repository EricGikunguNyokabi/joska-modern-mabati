// document.addEventListener('DOMContentLoaded', function() {
//     const quantityInput = document.getElementById('quantity');
//     const totalPriceElement = document.getElementById('totalPrice');
//     const totalProductPriceInput = document.getElementById('total_product_price');
//     const pricePerUnit = parseFloat('{{ product_info[4] }}');

//     document.getElementById('minusBtn').addEventListener('click', function() {
//         let quantity = parseInt(quantityInput.value);
//         if (quantity > 1) {
//             quantity--;
//             quantityInput.value = quantity;
//             updateTotalPrice(quantity);
//         }
//     });

//     document.getElementById('addBtn').addEventListener('click', function() {
//         let quantity = parseInt(quantityInput.value);
//         quantity++;
//         quantityInput.value = quantity;
//         updateTotalPrice(quantity);
//     });

//     quantityInput.addEventListener('input', function() {
//         let quantity = parseInt(quantityInput.value);
//         if (isNaN(quantity) || quantity < 1) {
//             quantityInput.value = 1;
//             quantity = 1;
//         }
//         updateTotalPrice(quantity);
//     });

//     function updateTotalPrice(quantity) {
//         const totalPrice = pricePerUnit * quantity;
//         totalPriceElement.textContent = `KSh. ${totalPrice.toFixed(2)}`;
//         totalProductPriceInput.value = totalPrice.toFixed(2);
//     }
// });
// Wait until the document is fully loaded






// document.addEventListener('DOMContentLoaded', function() {
//     var cartItems = document.querySelectorAll('.cart-row');

//     // Event listener for quantity changes
//     cartItems.forEach(function(item) {
//         var quantityInput = item.querySelector('.cart-quantity-input');
//         quantityInput.addEventListener('change', function() {
//             var row = item;
//             var quantity = parseInt(quantityInput.value);
//             if (isNaN(quantity) || quantity < 1) {
//                 quantity = 1;
//                 quantityInput.value = 1;
//             }
//             updateTotal(row);
//             updateCartTotal();
//         });
//     });

//     // Event listener for remove buttons
//     var removeButtons = document.querySelectorAll('.btn-danger');
//     removeButtons.forEach(function(button) {
//         button.addEventListener('click', function(event) {
//             var row = event.target.closest('.cart-row');
//             row.remove();
//             updateCartTotal();
//         });
//     });

//     // Event listener for clear cart button
//     document.querySelector('.btn-clear').addEventListener('click', function() {
//         var cartItemsContainer = document.querySelector('.cart-items');
//         while (cartItemsContainer.firstChild) {
//             cartItemsContainer.removeChild(cartItemsContainer.firstChild);
//         }
//         updateCartTotal();
//     });

//     // Function to update total price for a row
//     function updateTotal(row) {
//         var priceElement = row.querySelector('.cart-price');
//         var quantityElement = row.querySelector('.cart-quantity-input');
//         var totalElement = row.querySelector('.cart-total');
//         var price = parseFloat(priceElement.innerText.replace('KSh. ', '').replace(',', ''));
//         var quantity = parseInt(quantityElement.value);
//         var total = price * quantity;
//         totalElement.innerText = 'KSh. ' + total.toFixed(2);
//     }

//     // Function to update the overall cart total
//     function updateCartTotal() {
//         var cartRows = document.querySelectorAll('.cart-row');
//         var total = 0;
//         cartRows.forEach(function(row) {
//             var totalElement = row.querySelector('.cart-total');
//             var totalPrice = parseFloat(totalElement.innerText.replace('KSh. ', '').replace(',', ''));
//             total += totalPrice;
//         });
//         document.querySelector('.cart-total-price').innerText = 'KSh. ' + total.toFixed(2);
//     }
// });

{/* <script> */}
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
});
{/* </script> */}
