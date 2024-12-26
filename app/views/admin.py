import os
from flask import Blueprint, render_template, request, flash, current_app, redirect, url_for
from werkzeug.utils import secure_filename
from app.models.product import Product, Category  # Ensure you have a Product model defined
from app.models.user import User
from app.models.order import Order, OrderItem
from app import db
import os
from datetime import datetime

admin = Blueprint("admin",__name__)



# Route for Admin Dashboard
@admin.route("/adm/dash")
def admin_dashboard():
    # Quick stats
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()

    # Fetch recent activities: latest 5 orders, products, and users
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(5).all()
    recent_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()

    return render_template(
        "admin/dashboard.html",
        total_products=total_products,
        total_orders=total_orders,
        total_users=total_users,
        recent_orders=recent_orders,
        recent_products=recent_products,
        recent_users=recent_users
    )


# DISPLAY PRODUCTS BEFORE EDIT
@admin.route("/adm/products/edit-products")
def edit_products():
    categories = Category.query.all()
    products = Product.query.all()
    return render_template("admin/edit_products.html", products=products, categories=categories)

# EDIT PRODUCT ROUTE 1 BY 1
@admin.route("/adm/product/edit/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    # Fetch the product and all categories
    product = Product.query.get_or_404(product_id)
    categories = Category.query.all()

    if request.method == "POST":
        # Form fields from the request
        product_name = request.form["product_name"]
        product_category = request.form["product_category"]
        product_description = request.form["product_description"]
        product_cost = request.form["product_cost"]
        product_image = request.files.get("product_image")  # Fetch the uploaded file if present

        # Map the category name to category ID
        category_map = {
            "Roofing": 1,
            "Gutter System": 2,
            "Our Work": 3
        }
        product_category_id = category_map.get(product_category)

        if not product_category_id:
            flash("Invalid product category selected.", "danger")
            return render_template("admin/edit_product_form.html", product=product, categories=categories)

        # Update the product details
        product.product_name = product_name
        product.product_category = product_category
        product.product_category_id = product_category_id
        product.product_description = product_description
        product.product_cost = product_cost

        # Update the image if a new file is uploaded
        if product_image and product_image.filename:
            image_filename = secure_filename(product_image.filename)
            upload_folder = current_app.config["PRODUCT_UPLOAD_FOLDER"]
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, image_filename)
            product_image.save(image_path)

            # Update the image path in the database
            product.product_image_path = f"images/products/{image_filename}"

            print(f"\n\n EDIT IMAGE {product.product_image_path}")

        # Commit updates to the database
        try:
            db.session.commit()
            flash("Product updated successfully!", "success")
            return redirect(url_for("admin.edit_products"))
        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while updating the product: {str(e)}", "danger")

    # Render the form with pre-filled product details
    return render_template("admin/edit_product_form.html", product=product, categories=categories)

# @admin.route("/adm/product/edit/<int:product_id>", methods=["GET", "POST"])
# def edit_product(product_id):
#     # Fetch the product and all categories
#     product = Product.query.get_or_404(product_id)  
#     categories = Category.query.all()

    

#     if request.method == "POST":
#         # Form fields from the request
#         product_name = request.form["product_name"]
#         product_category = request.form["product_category"]
#         product_description = request.form["product_description"]
#         product_cost = request.form["product_cost"]
#         product_image_path = request.form["product_image_path"]

#         # Map the category name to category ID
#         category_map = {
#             "Roofing": 1,
#             "Gutter System": 2,
#             "Our Work": 3
#         }
#         product_category_id = category_map.get(product_category)

#         if not product_category_id:
#             flash("Invalid product category selected.", "danger")
#             return render_template("admin/edit_product_form.html", product=product, categories=categories)

#         # Update the product details
#         product.product_name = product_name
#         product.product_category = product_category
#         product.product_category_id = product_category_id  # Update category ID
#         product.product_description = product_description
#         product.product_cost = product_cost
#         product.product_image_path = product_image_path

#         # Commit updates to the database
#         try:
#             db.session.commit()
#             flash("Product updated successfully!", "success")
#             return redirect(url_for("admin.edit_products"))
#         except Exception as e:
#             db.session.rollback()
#             flash(f"An error occurred while updating the product: {str(e)}", "danger")

#     # Render the form with pre-filled product details
#     return render_template("admin/edit_product_form.html", product=product, categories=categories)




@admin.route("/adm/dash/manage-orders", methods=["GET", "POST"])
def manage_orders():
    # Fetch all orders
    orders = Order.query.order_by(Order.order_date.desc()).all()

    if request.method == "POST":
        # Handle updates for an order status
        order_id = request.form.get("order_id")
        action = request.form.get("action")  # Expected values: seen, sorted, delete

        try:
            order = Order.query.get(order_id)
            if not order:
                flash(f"Order #{order_id} not found.", "danger")
                return redirect(url_for("admin.manage_orders"))

            if action == "seen":
                order.status = "Seen"
                order.updated_at = datetime.now()
                db.session.commit()
                flash(f"Order #{order_id} marked as 'Seen'.", "success")

            elif action == "delivered":
                order.status = "Delivered"
                order.updated_at = datetime.now()
                db.session.commit()
                flash(f"Order #{order_id} marked as 'Delivered'.", "success")

            elif action == "delete":
                db.session.delete(order)
                db.session.commit()
                flash(f"Order #{order_id} has been deleted.", "danger")

            else:
                flash("Invalid action.", "warning")

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")

        return redirect(url_for("admin.manage_orders"))

    return render_template("admin/manage_orders.html", orders=orders)



@admin.route("/adm/dash/manage-users")
def manage_users():
    pass

@admin.route("/adm/dash/manage-privileges")
def manage_privileges():
    pass



# CATEGORY ROUTES

@admin.route("/category/add-category", methods=["POST", "GET"])
def add_category_details():
    if request.method == "POST":
        try:
            # Retrieve form data
            category_name = request.form.get("category_name")
            category_image = request.files.get("category_image_path")

            # Validate required fields
            if not all([category_name, category_image]):
                flash("All fields are required, including an image!", "danger")
                return render_template("admin/add_category.html")

            # Secure file upload
            image_filename = secure_filename(category_image.filename)
            upload_folder = current_app.config["CATEGORY_UPLOAD_FOLDER"]
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, image_filename)
            category_image.save(image_path)

            # Save category to the database using SQLAlchemy
            new_category = Category(
                category_name=category_name,
                category_image_path=f"images/category/{image_filename}"  # Relative path for the database
            )
            db.session.add(new_category)
            db.session.commit()

            flash(f"Category '{category_name}' added successfully!", "success")
            return redirect(url_for('admin.add_category_details'))  # Redirect after successful submission

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")
            return render_template("admin/add_category.html")

    return render_template("admin/add_category.html")