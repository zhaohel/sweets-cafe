import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_simple_message():
    api_key = os.getenv("MAILGUN_API_KEY")
    domain = "sandbox265e7a36f12c49fcbac09ff70886ef50.mailgun.org"

    print("DOMAIN:", domain)

    response = requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", api_key),
        data={
            "from": f"Mailgun Sandbox <postmaster@{domain}>",
            "to": "helenayizhao@gmail.com",
            "subject": "Mailgun Test Email",
            "text": "If you received this, Mailgun is working!"
        }
    )

    print("Status Code:", response.status_code)
    print("Response:", response.text)


send_simple_message()