from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()

def get_client():
    return Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )

def send_whatsapp(to_phone, message):
    try:
        client = get_client()

        if not to_phone.startswith('whatsapp:'):
            to_phone = f'whatsapp:{to_phone}'

        msg = client.messages.create(
            from_='whatsapp:+14155238886',
            to=to_phone,
            body=message
        )

        print("WhatsApp sent:", msg.sid)

    except Exception as e:
        print("WhatsApp error:", e)


# 📩 Templates

def appointment_confirmation_msg(name, doctor, date):
    return f"""
Hello {name} 👋

Your appointment is confirmed ✅
Doctor: Dr. {doctor}
Date: {date}

- Pushpa Dental Clinic
"""

def appointment_cancelled_msg(name, doctor, date):
    return f"""
Hello {name}

Your appointment with Dr. {doctor} on {date} is cancelled ❌

- Clinic
"""
def appointment_reminder_msg(name, doctor, date):
    return f"""
Hello {name} ⏰

Reminder: You have an appointment tomorrow

Doctor: Dr. {doctor}
Date: {date}

- Pushpa Dental Clinic
"""