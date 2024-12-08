import os
from flask import Blueprint, render_template, request, flash, current_app
from werkzeug.utils import secure_filename
from app.models.product import Product  # Ensure you have a Product model defined
from app import db

ecommerce = Blueprint('ecommerce', __name__)

@ecommerce.route('/')
def home():
    products = Product.query.all()  # Fetch all products from the database
    return render_template('home.html', products=products)

@ecommerce.route('/products')
def all_products():
    products = Product.query.all()  # Fetch all products from the database
    return render_template('product/all_products.html', products=products)


@ecommerce.route("/product/add-product", methods=["POST", "GET"])
def add_product_details():
    if request.method == "POST":
        try:
            # Retrieve form data
            product_category = request.form.get("product_category")
            product_name = request.form.get("product_name")
            product_description = request.form.get("product_description")
            product_cost = request.form.get("product_cost")
            product_image = request.files.get("product_image_path")

            # Validate required fields
            if not all([product_category, product_name, product_cost, product_image]):
                flash("All fields are required, including an image!", "danger")
                return render_template("admin/add_product.html")

            # Validate numeric field
            try:
                product_cost = float(product_cost)
            except ValueError:
                flash("Product cost must be a valid number.", "danger")
                return render_template("admin/add_product.html")

            # Secure file upload
            image_filename = secure_filename(product_image.filename)
            upload_folder = current_app.config["UPLOAD_FOLDER"]
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, image_filename)
            product_image.save(image_path)

            # Save product to the database using SQLAlchemy
            new_product = Product(
                product_category=product_category,
                product_name=product_name,
                product_description=product_description,
                product_cost=product_cost,
                product_image_path=f"images/products/{image_filename}"  # Relative path for the database
            )
            db.session.add(new_product)
            db.session.commit()

            flash(f"Product '{product_name}' added successfully!", "success")
            return render_template("admin/add_product.html")

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")
            return render_template("admin/add_product.html")

    return render_template("admin/add_product.html")

# SINGLE ITEM VIEW
@ecommerce.route('/product/<int:product_id>')
def single_product_detail(product_id):
    product = Product.query.get_or_404(product_id)  # Fetch product by ID
    return render_template('product/single_product.html', product=product)