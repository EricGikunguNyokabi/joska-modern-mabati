from app import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), default="Pending")
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


    # One-to-Many relationship to OrderItem
    items = db.relationship("OrderItem", backref="order", lazy=True)

    def __repr__(self):
        return f"<Order {self.order_id} - {self.contact_number}>"


class OrderItem(db.Model):
    __tablename__ = "order_items"

    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<OrderItem {self.product_name} (x{self.quantity})>"
