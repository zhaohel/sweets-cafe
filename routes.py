from flask import render_template, request, redirect, flash
from models import Order, OrderItem, MenuItem
from extensions import db
from notifications import send_order_notifications, send_contact_message


def register_routes(app):

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/order", methods=["GET", "POST"])
    def order():

        if request.method == "POST":

            name = request.form.get("customer_name")
            customer_email = request.form.get("email")

            mantou = int(request.form.get("mantou", 0))
            snowflake = int(request.form.get("snowflake", 0))
            youtiao = int(request.form.get("youtiao", 0))
            banana = int(request.form.get("banana", 0))
            cheesefoam = int(request.form.get("cheesefoam", 0))
            strawberry = int(request.form.get("strawberry", 0))

            if (
                mantou == 0 and
                snowflake == 0 and
                youtiao == 0 and
                banana == 0 and
                cheesefoam == 0 and
                strawberry == 0
            ):
                flash("Please select at least one item.")
                return redirect("/order")

            order = Order(
                customer_name=name,
                customer_email=customer_email,
                total_price=0
            )

            db.session.add(order)
            db.session.flush()

            total_price = 0

            def add_item(item_name, quantity):
                nonlocal total_price

                if quantity > 0:
                    menu_item = MenuItem.query.filter_by(name=item_name).first()

                    if not menu_item:
                        return 

                    price = menu_item.price
                    line_total = price * quantity
                    total_price += line_total

                    db.session.add(OrderItem(
                        order_id=order.id,
                        item_name=item_name,
                        quantity=quantity,
                        price_each=price,
                        line_total=line_total
                    ))

            add_item("Mantou", mantou)
            add_item("Snowflake Crisps", snowflake)
            add_item("Youtiao", youtiao)
            add_item("Banana Matcha", banana)
            add_item("Cheesefoam Matcha", cheesefoam)
            add_item("Strawberry Matcha", strawberry)

            order.total_price = total_price

            db.session.commit()

            success = send_order_notifications(order, "helenayizhao@gmail.com")

            if success:
                flash("Order placed successfully!")
            else:
                flash("Order saved but email may have failed.")

            return redirect("/order")

        menu_items = MenuItem.query.all()
        menu_dict = {item.name: item.price for item in menu_items}
        return render_template("order.html", menu_dict=menu_dict)

    @app.route("/contact", methods=["GET", "POST"])
    def contact():

        if request.method == "POST":
            name = request.form.get("name")
            sender_email = request.form.get("email")
            message_body = request.form.get("message")

            success = send_contact_message(name, sender_email, message_body)

            if success:
                flash("Message sent successfully!")
            else:
                flash("Email failed to send.")

            return redirect("/contact")

        return render_template("contact.html")