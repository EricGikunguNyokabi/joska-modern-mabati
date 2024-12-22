from flask import Blueprint, render_template, redirect, url_for, request, jsonify, session,flash

# models
from app.models.product import Product
from app.models.order import Order, OrderItem
# 
from flask_login import login_required
from flask_mail import Message
from app import db, mail
from twilio.rest import Client
from flask import current_app

cart = Blueprint("cart", __name__)


# Helper function to get total cart item count
def get_cart_item_count():
    if "cart" in session:
        return sum(item["quantity"] for item in session["cart"])
    return 0


# Endpoint to fetch real-time cart item count
# @cart.route("/cart-count", methods=["GET"])
# def cart_count():
#     item_count = get_cart_item_count()
#     return jsonify({"count": item_count}), 200


# @cart.route("/cart", methods=["GET", "POST"])
# def cart_content():
#     if "cart" not in session:
#         session["cart"] = []

#     if request.method == "GET":
#         total_price = sum(item["price"] * item["quantity"] for item in session["cart"])

#         # # Calculate the total count by summing up the quantities of all items
#         # total_cart_items = sum(item['quantity'] for item in cart)
#         # Calculate the total count by summing up the quantities of all items
#         total_cart_items = sum(item['quantity'] for item in session["cart"])
        
#         return render_template(
#             "product/cart/cart.html",
#             cart_items=session["cart"],
#             total_price=total_price,
#             total_cart_items=total_cart_items,
#             success=True,
#         )

#     if request.method == "POST" and request.is_json:
#         data = request.get_json()
#         product_id = data.get("product_id")
#         action = data.get("action", "increment")  # Default to "increment" if not provided

#         if product_id:
#             product = Product.query.filter_by(product_id=product_id).first()
#             if product:
#                 item_found = False
#                 for item in session["cart"]:
#                     if item["product_id"] == product.product_id:
#                         item_found = True
#                         if action == "increment":
#                             item["quantity"] += 1
#                         elif action == "decrement" and item["quantity"] > 0:
#                             item["quantity"] -= 1
                        
#                         # Remove item if quantity is zero
#                         if item["quantity"] == 0:
#                             session["cart"].remove(item)

#                         session.modified = True

#                         # Calculate updated data for response
#                         updated_quantity = item["quantity"]
#                         updated_item_total = item["price"] * item["quantity"] if updated_quantity > 0 else 0
#                         total_price = sum(it["price"] * it["quantity"] for it in session["cart"])
#                         cart_empty = len(session["cart"]) == 0

#                         return jsonify({
#                             "success": True,
#                             "updated_quantity": updated_quantity,
#                             "updated_item_total": updated_item_total,
#                             "new_total_price": total_price,
#                             "cart_empty": cart_empty
#                         }), 200

#                 # If product is not found in the cart, initialize with 1 quantity (adding it)
#                 session["cart"].append({
#                     "product_id": product.product_id,
#                     "product_image_path":product.product_image_path,
#                     "name": product.product_name,
#                     "price": product.product_cost,
#                     "quantity": 1
#                 })
#                 session.modified = True

#                 return jsonify({
#                     "success": True,
#                     "message": "Item added to cart (with zero quantity)."
#                 })

#     return jsonify({"success": False, "message": "Invalid request."}), 400

@cart.route("/cart", methods=["GET", "POST"])
def cart_content():
    if "cart" not in session:
        session["cart"] = []

    if request.method == "GET":
        total_price = sum(item["price"] * item["quantity"] for item in session["cart"])
        # Calculate the total item count by summing the quantities of all items
        total_cart_items = sum(item['quantity'] for item in session["cart"])
        
        # Render the cart template and pass the dynamic variables
        return render_template(
            "product/cart/cart.html",
            cart_items=session["cart"],
            total_price=total_price,
            total_cart_items=total_cart_items,  # Pass the cart item count to the template
            success=True,
        )

    if request.method == "POST" and request.is_json:
        data = request.get_json()
        product_id = data.get("product_id")
        action = data.get("action", "increment")  # Default to increment action if none specified

        # Logic to handle adding or updating cart items
        if product_id:
            product = Product.query.filter_by(product_id=product_id).first()
            if product:
                item_found = False
                for item in session["cart"]:
                    if item["product_id"] == product.product_id:
                        item_found = True
                        if action == "increment":
                            item["quantity"] += 1
                        elif action == "decrement" and item["quantity"] > 0:
                            item["quantity"] -= 1
                        
                        # Remove item if quantity is zero
                        if item["quantity"] == 0:
                            session["cart"].remove(item)

                        session.modified = True

                        # Calculate updated data for response
                        updated_quantity = item["quantity"]
                        updated_item_total = item["price"] * item["quantity"] if updated_quantity > 0 else 0
                        total_price = sum(it["price"] * it["quantity"] for it in session["cart"])
                        cart_empty = len(session["cart"]) == 0

                        return jsonify({
                            "success": True,
                            "updated_quantity": updated_quantity,
                            "updated_item_total": updated_item_total,
                            "new_total_price": total_price,
                            "cart_empty": cart_empty
                        }), 200

                # If product is not already in cart, add with initial quantity of 1
                session["cart"].append({
                    "product_id": product.product_id,
                    "product_image_path": product.product_image_path,
                    "name": product.product_name,
                    "price": product.product_cost,
                    "quantity": 1
                })
                session.modified = True

                return jsonify({
                    "success": True,
                    "message": "Item added to cart."
                })

    return jsonify({"success": False, "message": "Invalid request."}), 400



@cart.route("/cart-count", methods=["GET"])
def cart_count():
    # Calculate the total item count by summing the quantity of all items in the cart session
    total_items = sum(item["quantity"] for item in session.get("cart", []))
    
    # Print the total cart item count to the console (for debugging)
    print(f"total_items: {total_items}")
    
    # Return the count in JSON format for the AJAX call
    return jsonify({"count": total_items}), 200


# @cart.route('/increment-cart-item', methods=['POST'])
# def increment_cart_item():
#     data = request.get_json()

#     product_id = data.get('product_id')
#     quantity = data.get('quantity')

#     # Log the incoming request data for debugging
#     cart.logger.debug(f"Product ID: {product_id}, Quantity: {quantity}")

#     # Retrieve the cart from the session, if it exists
#     cart = session.get('cart', {})

#     # Log the cart to debug its contents
#     cart.logger.debug(f"Cart Contents: {cart}")

#     if product_id in cart:
#         cart_item = cart[product_id]
#         cart_item['quantity'] = quantity  # Update quantity
#         cart[product_id] = cart_item  # Save updated item in cart
#         session['cart'] = cart  # Save the updated cart
        
#         # Calculate total price and item count
#         total_price = sum(item['price'] * item['quantity'] for item in cart.values())
#         item_count = sum(item['quantity'] for item in cart.values())

#         return jsonify({'success': True, 'total_price': total_price, 'item_count': item_count})
#     else:
#         cart.logger.debug(f"Item not found in cart for product_id {product_id}")
#         return jsonify({'success': False, 'message': 'Item not found in cart'}), 404







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



# Route to display and place an order
@cart.route("/place-order", methods=["GET", "POST"])
def place_order():
    cart_items = session.get("cart", [])
    if not cart_items:
        return redirect(url_for("cart.cart_content"))

    total_price = sum(item["price"] * item["quantity"] for item in cart_items)

    if request.method == "POST":
        return redirect(url_for("cart.finalize_order"))

    return render_template(
        "product/cart/place_order.html", cart_items=cart_items, total_price=total_price
    )





def cartapp_message(order_details, recipient):
    client = Client(current_app.config["TWILIO_ACCOUNT_SID"], current_app.config["TWILIO_AUTH_TOKEN"])

    # Generate message body
    items_list = "\n".join(
        [f"- {item['name']} x{item['quantity']} @ KSh {item['price']:,}" for item in order_details['cart_items']]
    )

    message_body = (
        f"*Thank you for your order from {current_app.config['COMPANY_NAME']}!*\n\n"
        f"_Shipping Address:_ {order_details['shipping_address']}\n"
        f"_Contact Number:_ {order_details['contact_number']}\n\n"
        f"*Order Items:*\n{items_list}\n\n"
        f"*Total Price:* KSh {order_details['total_price']:,}\n\n"
        f"For support, contact us at: {current_app.config['COMPANY_PHONE_1']} or {current_app.config['COMPANY_EMAIL_1']}"
    )

    # Print the message body to check
    print("Sending WhatsApp message:\n", message_body)

    # Send WhatsApp message
    try:
        message = client.messages.create(
            body=message_body,
            from_=current_app.config["TWILIO_WHATSAPP_NUMBER"],
            to=f"whatsapp:{recipient}",
        )
        print("WhatsApp message sent successfully!", message.sid)  # Log the success message
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")



@cart.route('/send-whatsapp')
def send_whatsapp_message():
    # Phone number you want to send to (must be in WhatsApp format)
    to_phone_number = "whatsapp:+254701838170"  # Ensure this number is verified

    try:
        # Send the WhatsApp message using the Twilio client
        message = current_app.twilio_client.messages.create(
            body="Hello from Flask + Twilio!",  # The message body
            from_=current_app.config['TWILIO_WHATSAPP_NUMBER'],  # Your Twilio WhatsApp number
            to=to_phone_number  # Recipient's phone number
        )
        return f"Message sent successfully! Message SID: {message.sid}"

    except Exception as e:
        return f"Failed to send message. Error: {str(e)}"




@cart.route("/finalize-order", methods=["GET", "POST"])
def finalize_order():
    # Retrieve order details
    shipping_address = request.form.get("shipping_address")
    contact_number = request.form.get("contact_number")
    cart_items = session.get("cart", [])
    total_price = sum(item["price"] * item["quantity"] for item in cart_items)

    # Redirect if essential details are missing
    if not shipping_address or not contact_number:
        flash("Missing required fields! Shipping address and contact number are mandatory.", "danger")
        return redirect(url_for("cart.place_order"))

    try:
        # Step 1: Save the main order record to the database
        order = Order(
            shipping_address=shipping_address,
            contact_number=contact_number,
            total_price=total_price
        )
        db.session.add(order)
        db.session.flush()  # Allows fetching 'order_id' without committing yet

        # Step 2: Save all cart items (order items) to the database
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.order_id,
                product_id=item["product_id"],  # Corrected key
                product_name=item["name"],
                quantity=item["quantity"],
                price=item["price"],
            )
            db.session.add(order_item)

        # Step 3: Commit all database changes
        db.session.commit()

        # Step 4: Prepare order confirmation details
        order_details = {
            "order_id": order.order_id,
            "shipping_address": shipping_address,
            "contact_number": contact_number,
            "cart_items": cart_items,
            "total_price": total_price,
        }

        # Step 5: Send confirmation email
        try:
            msg = Message(
                subject=f"Order Confirmation - #{order.order_id}",
                recipients=["joskamabati@gmail.com", "nyokabigeric@gmail.com", "joskamodernmabati@gmail.com"],  # Emails for confirmation
                html=render_template("product/cart/order_success.html", order_details=order_details),
            )
            mail.send(msg)
        except Exception as e:
            print(f"Failed to send email: {e}")  # Email failure shouldn't break order finalization

        # Step 6: Send WhatsApp order confirmation (if configured)
        try:
            recipient = "+254701838170"  # Update dynamically if needed
            send_whatsapp_message(order_details, recipient)
        except Exception as e:
            print(f"Failed to send WhatsApp message: {e}")  # Log for debugging

        # Step 7: Clear cart session after successful order
        session.pop("cart", None)

        # Step 8: Display success page with order details
        return render_template("product/cart/order_success.html", order_details=order_details)

    except Exception as e:
        db.session.rollback()  # Rollback in case of errors
        print(f"Error finalizing order: {e}")
        flash("An error occurred while finalizing the order. Please try again.", "danger")
        return redirect(url_for("cart.place_order"))


# @cart.route("/finalize-order", methods=["GET", "POST"])
# def finalize_order():
#     # Retrieve order details
#     shipping_address = request.form.get("shipping_address")
#     contact_number = request.form.get("contact_number")
#     cart_items = session.get("cart", [])
#     total_price = sum(item["price"] * item["quantity"] for item in cart_items)

#     # Redirect if missing required information
#     if not shipping_address or not contact_number:
#         return redirect(url_for("cart.place_order"))

#     # Prepare order details
#     order_details = {
#         "shipping_address": shipping_address,
#         "contact_number": contact_number,
#         "cart_items": cart_items,
#         "total_price": total_price,
#     }

#     # Clear the cart from the session
#     session.pop("cart", None)

#     # Send order confirmation email
#     try:
#         msg = Message(
#             subject=f"Order Placed by - {order_details['contact_number']}",
#             recipients=[
#             # "joskamodernmabati@gmail.com",   # Company email
#             # "josekaush@gmail.com",
#             "nyokabigikungueric@gmail.com",
#             "nyokabigeric@gmail.com"  # Test email
#         ],
#             # recipients=["joskamodernmabati@gmail.com"],  # Company email
#             html=render_template("product/cart/order_success.html", order_details=order_details),
#         )
#         mail.send(msg)
#     except Exception as e:
#         print(f"Failed to send email: {e}")  # Handle email failures gracefully

#     # Send WhatsApp
#     try:
#         recipient = "+254701838170"  # Replace this with dynamic contact_number if customer is notified
#         send_whatsapp_message(order_details, recipient)
#     except Exception as e:
#         print(f"Failed to send WhatsApp message: {e}")

#     session.pop("cart", None)

#     # Render the success template for the customer
#     return render_template(
#         "product/cart/order_success.html", order_details=order_details
#     )


