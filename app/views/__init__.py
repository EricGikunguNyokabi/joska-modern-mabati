# views/__init__.py
from flask import Blueprint, render_template
from app.models.product import Product, Category

main = Blueprint('main', __name__)



@main.route('/')
def home():
    categories = Category.query.all()
    products = Product.query.all()  # Fetch all products from the database
    return render_template('home.html',categories=categories, products=products)