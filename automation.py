from datetime import datetime, timedelta
from models import db, Appointment, FestivalMessage, Patient
from whatsapp_utils import send_whatsapp


# ─────────────────────────────────────────────
# 1. APPOINTMENT REMINDER (Runs every 1 hour)
# ─────────────────────────────────────────────
def send_appointment_reminders(app):
    with app.app_context():
        now = datetime.now()
        upcoming = now + timedelta(hours=2)

        appointments = Appointment.query.filter(
            Appointment.appointment_date.between(now, upcoming),
            Appointment.status == "scheduled"
        ).all()

        for a in appointments:
            msg = f"Reminder: Your appointment with Dr. {a.doctor.name} is at {a.appointment_date}"
            send_whatsapp(a.patient.phone, msg)


# ─────────────────────────────────────────────
# 2. FESTIVAL AUTO MESSAGE
# ─────────────────────────────────────────────
def send_festival_messages(app):
    with app.app_context():
        today = datetime.now().date()

        festivals = FestivalMessage.query.filter_by(festival_date=today).all()
        patients = Patient.query.all()

        for f in festivals:
            for p in patients:
                msg = f.message_template.replace("{name}", p.name)
                send_whatsapp(p.phone, msg)


# ─────────────────────────────────────────────
# 3. DAILY DOCTOR SCHEDULE
# ─────────────────────────────────────────────
def send_daily_schedule(app):
    from models import Doctor

    with app.app_context():
        today = datetime.now().date()

        doctors = Doctor.query.all()

        for d in doctors:
            appointments = Appointment.query.filter(
                Appointment.doctor_id == d.id,
                Appointment.appointment_date >= today
            ).all()

            if appointments:
                msg = f"Today's schedule for Dr. {d.name}:\n"
                for a in appointments:
                    msg += f"- {a.patient.name} at {a.appointment_date}\n"

                # optional doctor phone if added later