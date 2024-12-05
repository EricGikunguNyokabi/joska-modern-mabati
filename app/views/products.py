# views/products.py
from flask import Blueprint, render_template
from app.models.product import Product  # Ensure you have a Product model defined

ecommerce = Blueprint('ecommerce', __name__)

@ecommerce.route('/')
def home():
    products = Product.query.all()  # Fetch all products from the database
    return render_template('home.html', products=products)

@ecommerce.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)  # Fetch product by ID
    return render_template('product_detail.html', product=product)