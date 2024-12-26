import os
from flask import Blueprint, render_template, request, flash, current_app
from werkzeug.utils import secure_filename
from app.models.product import Product, Category  # Ensure you have a Product model defined
from app import db

ecommerce = Blueprint("ecommerce", __name__)

@ecommerce.route('/')
def home():
    categories = Category.query.all() # Fetch all the categories from the database
    products = Product.query.all()  # Fetch all products from the database
    return render_template('home.html',categories=categories,  products=products)

@ecommerce.route("/products")
def all_products():
    # categories are ordered by their category_id
    categories = Category.query.order_by(Category.category_id).all()
    # products = Product.query.all() 

    # Number of products per page
    per_page = 100

    # Get the current page number, defaulting to 1 if not provided
    page = request.args.get('page', 1, type=int)

    # Query products and order them by product_category_id first, then product_id
    products = Product.query.order_by(Product.product_category_id, Product.product_id) \
                            .paginate(page=page, per_page=per_page, error_out=False)
    return render_template('product/all_products.html',categories=categories, products=products)

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

            # Map product category to product_category_id
            category_map = {
                "Roofing" : 1,
                "Gutter System" : 2,
                "Our Work" : 3
            }

            product_category_id = category_map.get(product_category)

            # Validate required fields
            if not all([product_category,product_category_id, product_name, product_cost, product_image]):
                flash("All fields are required, including an image!", "danger")
                return render_template("product/add_product.html")

            # Validate numeric field
            try:
                product_cost = float(product_cost)
            except ValueError:
                flash("Product cost must be a valid number.", "danger")
                return render_template("product/add_product.html")

            # Secure file upload
            image_filename = secure_filename(product_image.filename)
            upload_folder = current_app.config["PRODUCT_UPLOAD_FOLDER"]
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, image_filename)
            product_image.save(image_path)

            # Save product to the database using SQLAlchemy
            new_product = Product(
                product_category_id = product_category_id,
                product_category=product_category,
                product_name=product_name,
                product_description=product_description,
                product_cost=product_cost,
                product_image_path=f"images/products/{image_filename}"  # Relative path for the database
            )
            db.session.add(new_product)
            db.session.commit()

            flash(f"Product '{product_name}' added successfully!", "success")
            return render_template("product/add_product.html")

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", "danger")
            return render_template("product/add_product.html")

    return render_template("product/add_product.html")

# SINGLE ITEM VIEW
@ecommerce.route('/product/<int:product_id>')
def single_product_detail(product_id):
    product = Product.query.get_or_404(product_id)  # Fetch product by ID
    return render_template('product/single_product.html', product=product)





# @ecommerce.route("/products/category/<int:category_id>")
# def category_products(category_id):
#     category = Category.query.get_or_404(category_id) # Fetch category by id
#     products = Product.query.filter_by(product_category=category.category_id)  # Fetch products in this category
#     return render_template("product/category_products.html", category=category,products=products)

# Route to display products by category
@ecommerce.route("/category/<int:category_id>")
def category_products(category_id):
    # Query category details
    category = Category.query.filter_by(category_id=category_id).first_or_404()
    categories = Category.query.all() 
    
    # Query products associated with this category
    products = Product.query.filter_by(product_category_id=category_id).all()

    return render_template(
        "product/category_products.html",
        category=category,
        products=products, 
        categories=categories
    )




