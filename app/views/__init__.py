# views/__init__.py
from flask import Blueprint, render_template
from app.models.product import Product  

ecommerce = Blueprint('ecommerce', __name__)

@ecommerce.route('/')
def home():
    products = Product.query.all()  # Fetch all products from the database
    return render_template('home.html', products=products)