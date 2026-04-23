# 🏥 Clinic Management System — Python + WhatsApp

## Features
- Add/manage patients & doctors
- Book appointments with instant WhatsApp confirmation
- Automatic appointment reminders (24 hours before)
- Festival WhatsApp messages to all patients on set date
- Clean web admin panel

---

## 📁 Project Structure

```
clinic_system/
├── app.py              ← Start the server (run this!)
├── models.py           ← Database tables
├── routes.py           ← All API endpoints
├── whatsapp_utils.py   ← WhatsApp send functions
├── scheduler.py        ← Auto reminders & festival messages
├── requirements.txt    ← Python packages
├── .env                ← Your secret keys (DO NOT share)
└── templates/
    └── index.html      ← Web admin panel
```

---

## 🚀 Setup (Step by Step)

### Step 1 — Install Python packages
```bash
pip install -r requirements.txt
```

### Step 2 — Setup Twilio WhatsApp

1. Go to https://www.twilio.com → Sign up free
2. In the dashboard, click **Messaging → Try it out → Send a WhatsApp message**
3. You'll see a sandbox number like: `+14155238886`
4. Patient must send this join message first (sandbox only):
   ```
   join <your-sandbox-word>
   ```
5. Copy your **Account SID** and **Auth Token** from the dashboard

### Step 3 — Configure .env file
Open `.env` and fill in your credentials:
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

### Step 4 — Run the server
```bash
python app.py
```

Open your browser: **http://localhost:5000**

---

## 🔑 Common Mistakes & Fixes

| Mistake | Fix |
|---------|-----|
| Phone number without +91 | Always save as +919876543210 |
| Patient not receiving message | They must join sandbox first |
| Reminder sent twice | The reminder_sent flag prevents this |
| Festival sent to wrong patients | Check festival_date format YYYY-MM-DD |
| Scheduler not working | Don't use debug=True with reloader (already fixed in app.py) |

---

## 📱 WhatsApp Message Flow

```
Book Appointment → Instant Confirmation WhatsApp
24 hrs before    → Automatic Reminder WhatsApp
Festival date    → Festival Wishes to ALL patients
Cancel appt      → Cancellation Notice WhatsApp
```

---

## 🌟 Upgrade to Production WhatsApp (After Testing)

When ready to go live (no more sandbox):
1. Apply for WhatsApp Business API at https://www.twilio.com/whatsapp
2. Get a real phone number approved
3. Update TWILIO_WHATSAPP_FROM in .env with your approved number
4. Patients no longer need to "join" — messages go directly

---

## 🖥️ Deploying on a Server (so scheduler runs 24/7)

```bash
# Install on Ubuntu server
pip install -r requirements.txt
pip install gunicorn

# Run with gunicorn
gunicorn -w 1 -b 0.0.0.0:5000 "app:create_app()"

# Keep running always (use PM2 or systemd)
# Using nohup:
nohup python app.py &
```
