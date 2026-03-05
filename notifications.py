import requests
import os

def send_order_notifications(order, owner_email):
    api_key = os.getenv("MAILGUN_API_KEY")
    domain = os.getenv("MAILGUN_DOMAIN")

    if not api_key or not domain:
        return False

    item_text = "\n".join(
    f"- {item.item_name} x{item.quantity} (${item.line_total:.2f})"
    for item in order.items
    )

    owner_response = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={
            "from": f"Sweets Cafe <postmaster@{domain}>",
            "to": owner_email,
            "subject": f"New Order from {order.customer_name}",
            "text": f"""
New Order Received

Customer Name: {order.customer_name}
Customer Email: {order.customer_email}

Items Ordered:
{item_text}

Total: ${order.total_price:.2f}
"""
        }
    )

    customer_response = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={
            "from": f"Sweets Cafe <postmaster@{domain}>",
            "to": order.customer_email,
            "subject": "Your Sweets Cafe Order Receipt",
            "text": f"""
Hi {order.customer_name},

Thank you for your order!

Items Ordered:
{item_text}

- Sweets Cafe
"""
        }
    )

    return owner_response.status_code == 200 and customer_response.status_code == 200


def send_contact_message(name, sender_email, message_body):
    api_key = os.getenv("MAILGUN_API_KEY")
    domain = os.getenv("MAILGUN_DOMAIN")

    if not api_key or not domain:
        return False

    response = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={
            "from": f"Contact Form <postmaster@{domain}>",
            "to": ["helenayizhao@gmail.com", sender_email],
            "subject": f"New Contact Message from {name}",
            "text": f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message_body}"
        }
    )

    return response.status_code == 200