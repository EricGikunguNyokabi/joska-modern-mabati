# views/__init__.py
from flask import Blueprint, render_template, request
from app.models.product import Product, Category

main = Blueprint('main', __name__)



# @main.route('/')
# def home():
#     categories = Category.query.all()
#     products = Product.query.all()  # Fetch all products from the database
#     return render_template('home.html',categories=categories, products=products)
@main.route("/")
def home():
    categories = Category.query.all()

    # Number of products per page
    per_page = 3

    # Get the current page number, defaulting to 1 if not provided
    page = request.args.get('page', 1, type=int)

    # Query products and apply pagination with the correct arguments
    products = Product.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('home.html', categories=categories, products=products)

@main.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # Rollback any failed transactions
    return render_template('500.html'), 500
