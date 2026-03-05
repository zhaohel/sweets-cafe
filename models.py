from extensions import db
from datetime import datetime

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    total_price = db.Column(db.Float, nullable=False, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship(
        "OrderItem",
        backref="order",
        cascade="all, delete-orphan"
    )


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(
        db.Integer,
        db.ForeignKey("order.id"),
        nullable=False
    )

    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_each = db.Column(db.Float, nullable=False)
    line_total = db.Column(db.Float, nullable=False)