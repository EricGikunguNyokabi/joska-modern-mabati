# views/__init__.py
from flask import Blueprint, render_template, request
from app.models.product import Product, Category

main = Blueprint('main', __name__)



@main.route("/test")
def test():
    products = Product.query.all()
    print(f"Products: {products}")
    # print(f"Product Image Path: {product_image_path}")
    return render_template("test.html",products=products)


@main.route("/")
def home():
    # categories are ordered by their category_id
    categories = Category.query.order_by(Category.category_id).all()

    # Number of products per page
    per_page = 24

    # Get the current page number, defaulting to 1 if not provided
    page = request.args.get('page', 1, type=int)

    # Query products and order them by product_category_id first, then product_id
    products = Product.query.order_by(Product.product_category_id, Product.product_id) \
                            .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('home.html', categories=categories, products=products)


