from flask import Blueprint, render_template, redirect, url_for, request, jsonify, session
from app.models.product import Product
from flask_login import login_required

cart = Blueprint('cart', __name__)

# View for showing the cart contents
@cart.route("/cart", methods=["GET", "POST"])
def cart_content():
    # Ensure cart exists in the session
    if "cart" not in session:
        session["cart"] = []  # Initialize as an empty list

    # Handle POST request to add a product to the cart
    if request.method == "POST":
        # Check for JSON data (for AJAX)
        if request.is_json:
            data = request.get_json()
            product_id = data.get("product_id")
        else:
            # Handle form submission (standard POST request)
            product_id = request.form.get("product_id")

        if product_id:
            product = Product.query.filter_by(product_id=product_id).first()  # Retrieve the product
            if product:
                # Check if the product already exists in the cart (by product_id)
                product_exists = False
                for item in session["cart"]:
                    if item["product_id"] == product.product_id:
                        item["quantity"] += 1  # Increase the quantity
                        product_exists = True
                        break

                if not product_exists:
                    # Add the product to the cart if it doesn't exist yet
                    session["cart"].append({
                        "product_id": product.product_id,
                        "product_image_path": product.product_image_path,
                        "name": product.product_name,
                        "price": product.product_cost,
                        "quantity": 1  # Set initial quantity
                    })

                session.modified = True  # Mark session as modified

                if request.is_json:
                    return jsonify({"message": "Product added to cart!"}), 200
                else:
                    return redirect(url_for("cart.cart_content"))  # For non-AJAX requests

    # Handle GET request to view the cart
    cart_items = session.get("cart", [])
    
    # Calculate total price for the cart
    total_price = sum(item["price"] * item["quantity"] for item in cart_items)

    item = products = Product.query.all()
    return render_template("product/cart/cart.html", cart_items=cart_items, item=item, total_price=total_price)




# View for removing a product from the cart
@cart.route("/remove_from_cart/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart_items = session.get('cart', [])
    # Remove the product if it exists in the cart
    cart_items = [item for item in cart_items if item['product_id'] != product_id]
    session['cart'] = cart_items  # Update the session
    session.modified = True

    return redirect(url_for('cart.cart_content'))

# View for clearing the cart
@cart.route("/clear_cart", methods=["POST"])
def clear_cart():
    session.pop('cart', None)  # Clear the cart from session
    session.modified = True
    return redirect(url_for('cart.cart_content'))


# from flask import Blueprint, request, make_response, jsonify, render_template, session, redirect, url_for
# from flask_session import Session
# from app.models.product import Product, Category
# from flask_login import login_required
# import json

# cart = Blueprint("cart", __name__)


# @cart.route("/cart", methods=["GET", "POST"])
# def cart_content():
#     # Ensure cart exists in the session
#     if "cart" not in session:
#         session["cart"] = []  # Initialize as an empty list

#     # Handle POST request to add a product to the cart
#     if request.method == "POST":
#         # Check for JSON data (for AJAX)
#         if request.is_json:
#             data = request.get_json()
#             action = data.get("action")
#             product_id = data.get("product_id")
#             if action == "increase":
#                 # Increase the quantity of the product in the cart
#                 for item in session["cart"]:
#                     if item["product_id"] == product_id:
#                         item["quantity"] += 1
#                         break
#             elif action == "decrease":
#                 # Decrease the quantity of the product in the cart, but prevent negative quantity
#                 for item in session["cart"]:
#                     if item["product_id"] == product_id and item["quantity"] > 1:
#                         item["quantity"] -= 1
#                         break
#             elif action == "cancel":
#                 # Remove the product from the cart completely
#                 session["cart"] = [item for item in session["cart"] if item["product_id"] != product_id]

#             session.modified = True  # Mark session as modified
#             return jsonify({"cart": session["cart"]}), 200

#     # Handle GET request to view the cart
#     cart_items = session.get("cart", [])
    
#     # Calculate total price for the cart
#     total_price = sum(item["price"] * item["quantity"] for item in cart_items)
    
#     item = products = Product.query.all()
#     return render_template("product/cart/cart.html", cart_items=cart_items, item=item, total_price=total_price)






# @cart.route('/cart/update/<action>/<product_id>', methods=['POST'])
# def update_quantity(action, product_id):
#     if 'cart' not in session:
#         session['cart'] = []
    
#     product = Product.query.filter_by(product_id=product_id).first()
#     if not product:
#         return jsonify({'message': 'Product not found!'}), 404
    
#     # Find product in the cart session
#     cart_item = next((item for item in session['cart'] if item['product_id'] == product.product_id), None)
    
#     if cart_item:
#         if action == 'increment':
#             cart_item['quantity'] += 1
#         elif action == 'decrement' and cart_item['quantity'] > 1:
#             cart_item['quantity'] -= 1
#         session.modified = True  # Mark the session as modified to reflect the changes
    
#     return redirect(url_for('cart.cart_content'))





# # Remove single item 
# @cart.route('/cart/remove/<product_id>', methods=['POST'])
# def remove_item(product_id):
#     if 'cart' not in session:
#         session['cart'] = []

#     # Remove item from cart
#     session['cart'] = [item for item in session['cart'] if item['product_id'] != product_id]
#     session.modified = True  # Mark session as modified
#     return redirect(url_for('cart.cart_content'))



# @cart.route("/clear", methods=["POST"])
# def clear_cart():
#     """Clear all items from the shopping cart."""
#     session["cart"] = []  # Empty the cart
#     session.modified = True  # Mark the session as modified
#     return redirect(url_for("cart.cart_content"))  # Redirect back to cart view


@cart.route("/place-order", methods=["POST"])
def place_order():
    return redirect(url_for("cart.cart_content"))  # Redirect back to cart view






# # @cart.route('/add_to_cart', methods=['POST'])
# # def add_to_cart():
# #     """Add an item to the shopping cart."""
# #     product_id = request.json.get('product_id')
# #     quantity = request.json.get('quantity', 1)

# #     if not product_id:
# #         return jsonify({"error": "Product ID is required"}), 400

# #     # Get the current cart from cookies
# #     cart = request.cookies.get('cart')
# #     if cart:
# #         cart = json.loads(cart)
# #     else:
# #         cart = {}

# #     # Update the cart
# #     if product_id in cart:
# #         cart[product_id] += quantity
# #     else:
# #         cart[product_id] = quantity

# #     # Save the updated cart back to cookies
# #     response = make_response(jsonify({"message": "Item added to cart"}))
# #     response.set_cookie('cart', json.dumps(cart), httponly=True)  # Set cookie with httponly for security
# #     return response

# # @cart.route('/update_cart', methods=['POST'])
# # def update_cart():
# #     """Update the quantity of an item in the shopping cart."""
# #     product_id = request.json.get('product_id')
# #     quantity = request.json.get('quantity')

# #     if not product_id or quantity is None:
# #         return jsonify({"error": "Product ID and quantity are required"}), 400

# #     # Get the current cart from cookies
# #     cart = request.cookies.get('cart')
# #     if cart:
# #         cart = json.loads(cart)
# #     else:
# #         cart = {}

# #     # Update the cart
# #     if product_id in cart:
# #         if quantity <= 0:
# #             del cart[product_id]  # Remove item if quantity is zero or less
# #         else:
# #             cart[product_id] = quantity  # Update quantity
# #     else:
# #         return jsonify({"error": "Product not found in cart"}), 404

# #     # Save the updated cart back to cookies
# #     response = make_response(jsonify({"message": "Cart updated"}))
# #     response.set_cookie('cart', json.dumps(cart), httponly=True)
# #     return response

# # @cart.route('/remove_from_cart', methods=['POST'])
# # def remove_from_cart():
# #     """Remove an item from the shopping cart."""
# #     product_id = request.json.get('product_id')

# #     if not product_id:
# #         return jsonify({"error": "Product ID is required"}), 400

# #     # Get the current cart from cookies
# #     cart = request.cookies.get('cart')
# #     if cart:
# #         cart = json.loads(cart)
# #     else:
# #         cart = {}

# #     # Remove the item from the cart
# #     if product_id in cart:
# #         del cart[product_id]
# #     else:
# #         return jsonify({"error": "Product not found in cart"}), 404

# #     # Save the updated cart back to cookies
# #     response = make_response(jsonify({"message": "Item removed from cart"}))
# #     response.set_cookie('cart', json.dumps(cart), httponly=True)
# #     return response