# Imports
from flask import Flask
from dotenv import load_dotenv
import os
from extensions import db
from routes import register_routes

load_dotenv(override=True)

# My App
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orders.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

register_routes(app)

with app.app_context():
    db.create_all()

    from models import MenuItem

    if not MenuItem.query.first():
        items = [
            MenuItem(name="Mantou", price=3.00),
            MenuItem(name="Snowflake Crisps", price=4.50),
            MenuItem(name="Youtiao", price=3.00),
            MenuItem(name="Banana Matcha", price=6.50),
            MenuItem(name="Cheesefoam Matcha", price=6.50),
            MenuItem(name="Strawberry Matcha", price=6.75),
        ]
        db.session.add_all(items)
        db.session.commit()

#run locally
if __name__ == "__main__":
    app.run(debug=True)


#prodction 
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)