import json
from dotenv import load_dotenv
import os
import requests

# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

# Check for required environment variables
missing_vars = []
for var_name, var_value in [
    ("ACCESS_TOKEN", ACCESS_TOKEN),
    ("RECIPIENT_WAID", RECIPIENT_WAID),
    ("PHONE_NUMBER_ID", PHONE_NUMBER_ID),
    ("VERSION", VERSION),
]:
    if not var_value:
        missing_vars.append(var_name)

if missing_vars:
    print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
    exit(1)

# --------------------------------------------------------------
# Send a template WhatsApp message (requires approved template)
# --------------------------------------------------------------
def send_whatsapp_template_message():
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_WAID,
        "type": "template",
        "template": {"name": "smmart_contact", "language": {"code": "en"}},
    }
    response = requests.post(url, headers=headers, json=data)
    print("Template message response:")
    print(response.status_code)
    try:
        print(response.json())
    except Exception:
        print(response.text)
    return response

# --------------------------------------------------------------
# Send a custom text WhatsApp message
# --------------------------------------------------------------
def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )

def send_text_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"
    response = requests.post(url, data=data, headers=headers)
    print("Text message response:")
    print(response.status_code)
    try:
        print(response.json())
    except Exception:
        print(response.text)
    return response

if __name__ == "__main__":
    # Send a template message (uncomment if you want to test this and have a valid template)
    # send_whatsapp_template_message()

    # Send a custom text message
    data = get_text_message_input(
        recipient=RECIPIENT_WAID, text="Hello, this is a test message."
    )
    send_text_message(data)
