# views/__init__.py
from flask import Blueprint, render_template
from app.models.product import Product  

main = Blueprint('main', __name__)



@main.route('/')
def home():
    products = Product.query.all()  # Fetch all products from the database
    return render_template('home.html', products=products)