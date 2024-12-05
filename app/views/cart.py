from flask import Blueprint, request, make_response, jsonify, render_template
from flask_login import login_required
import json

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
@login_required
def cart():
    """Display the user's shopping cart."""
    cart = request.cookies.get('cart')
    if cart:
        cart = json.loads(cart)
    else:
        cart = {}

    return render_template('cart.html', cart=cart)

@cart_bp.route('/add_to_cart', methods=['POST'])
@login_required  # Ensure the user is logged in before adding to cart
def add_to_cart():
    """Add an item to the shopping cart."""
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity', 1)

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    # Get the current cart from cookies
    cart = request.cookies.get('cart')
    if cart:
        cart = json.loads(cart)
    else:
        cart = {}

    # Update the cart
    if product_id in cart:
        cart[product_id] += quantity
    else:
        cart[product_id] = quantity

    # Save the updated cart back to cookies
    response = make_response(jsonify({"message": "Item added to cart"}))
    response.set_cookie('cart', json.dumps(cart), httponly=True)  # Set cookie with httponly for security
    return response

@cart_bp.route('/update_cart', methods=['POST'])
@login_required  # Ensure the user is logged in before updating the cart
def update_cart():
    """Update the quantity of an item in the shopping cart."""
    product_id = request.json.get('product_id')
    quantity = request.json.get('quantity')

    if not product_id or quantity is None:
        return jsonify({"error": "Product ID and quantity are required"}), 400

    # Get the current cart from cookies
    cart = request.cookies.get('cart')
    if cart:
        cart = json.loads(cart)
    else:
        cart = {}

    # Update the cart
    if product_id in cart:
        if quantity <= 0:
            del cart[product_id]  # Remove item if quantity is zero or less
        else:
            cart[product_id] = quantity  # Update quantity
    else:
        return jsonify({"error": "Product not found in cart"}), 404

    # Save the updated cart back to cookies
    response = make_response(jsonify({"message": "Cart updated"}))
    response.set_cookie('cart', json.dumps(cart), httponly=True)
    return response

@cart_bp.route('/remove_from_cart', methods=['POST'])
@login_required  # Ensure the user is logged in before removing from the cart
def remove_from_cart():
    """Remove an item from the shopping cart."""
    product_id = request.json.get('product_id')

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    # Get the current cart from cookies
    cart = request.cookies.get('cart')
    if cart:
        cart = json.loads(cart)
    else:
        cart = {}

    # Remove the item from the cart
    if product_id in cart:
        del cart[product_id]
    else:
        return jsonify({"error": "Product not found in cart"}), 404

    # Save the updated cart back to cookies
    response = make_response(jsonify({"message": "Item removed from cart"}))
    response.set_cookie('cart', json.dumps(cart), httponly=True)
    return response