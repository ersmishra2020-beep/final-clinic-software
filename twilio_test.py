from twilio.rest import Client
import os

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

client = Client(account_sid, auth_token)

message = client.messages.create(
    from_="whatsapp:+14155238886",
    body="Hello from Flask Clinic System ✅ WhatsApp test working!",
    to="whatsapp:+91YOUR_NUMBER"
)

print("Message SID:", message.sid)