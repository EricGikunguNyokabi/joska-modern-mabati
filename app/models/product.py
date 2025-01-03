from app import db

class Category(db.Model):
    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False, unique=True)
    category_image_path = db.Column(db.String(255), nullable=True)  # Path for category image
    # One-to-Many relationship with Product
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.category_name}>"


class Product(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True)
    product_category = db.Column(db.String(100), nullable=False)
    product_category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    product_gauge = db.Column(db.String(255), nullable=True, default="") 
    product_name = db.Column(db.String(255), nullable=False)
    product_description = db.Column(db.Text, nullable=True)
    product_cost = db.Column(db.Float, nullable=False)
    product_image_path = db.Column(db.String(255), nullable=True)
    stock_quantity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __repr__(self):
        return f"<Product {self.product_name}>"