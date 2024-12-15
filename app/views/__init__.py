# views/__init__.py
from flask import Blueprint, render_template
from app.models.product import Product, Category

main = Blueprint('main', __name__)



@main.route('/')
def home():
    categories = Category.query.all()
    products = Product.query.all()  # Fetch all products from the database
    return render_template('home.html',categories=categories, products=products)

@main.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@main.errorhandler(500)
def internal_error(error):
    db.session.rollback()  # Rollback any failed transactions
    return render_template('500.html'), 500
