from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from whatsapp_utils import send_whatsapp, appointment_reminder_msg

scheduler = BackgroundScheduler()

def send_appointment_reminders(app):
    """
    Runs every hour.
    Finds appointments in the next 24 hours and sends WhatsApp reminders.
    """
    with app.app_context():
        from models import db, Appointment

        now = datetime.utcnow()
        tomorrow = now + timedelta(hours=24)

        # Find upcoming appointments with no reminder sent yet
        upcoming = Appointment.query.filter(
            Appointment.appointment_date >= now,
            Appointment.appointment_date <= tomorrow,
            Appointment.reminder_sent == False,
            Appointment.status == 'scheduled'
        ).all()

        print(f"[Scheduler] Checking reminders... Found {len(upcoming)} appointment(s) to remind.")

        for appt in upcoming:
            patient = appt.patient
            doctor = appt.doctor
            msg = appointment_reminder_msg(patient.name, doctor.name, appt.appointment_date)
            success = send_whatsapp(patient.phone, msg)
            if success:
                appt.reminder_sent = True
                db.session.commit()
                print(f"[Scheduler] Reminder sent to {patient.name} ({patient.phone})")


def send_festival_messages(app):
    """
    Runs every day at 8:00 AM.
    Checks if today is a festival and sends WhatsApp wishes to ALL patients.
    """
    with app.app_context():
        from models import db, FestivalMessage, Patient

        today = datetime.utcnow().date()

        festivals = FestivalMessage.query.filter_by(
            festival_date=today,
            sent=False
        ).all()

        if not festivals:
            print(f"[Scheduler] No festival today ({today}).")
            return

        patients = Patient.query.all()
        print(f"[Scheduler] Festival day! Sending to {len(patients)} patients.")

        for festival in festivals:
            for patient in patients:
                # Replace {name} in template with actual patient name
                msg = festival.message_template.replace('{name}', patient.name)
                send_whatsapp(patient.phone, msg)

            festival.sent = True
            db.session.commit()
            print(f"[Scheduler] Festival '{festival.festival_name}' messages sent!")


def start_scheduler(app):
    """Start all scheduled jobs."""

    # Appointment reminders — runs every hour
    scheduler.add_job(
        func=send_appointment_reminders,
        args=[app],
        trigger='interval',
        hours=1,
        id='appointment_reminders',
        replace_existing=True
    )

    # Festival messages — runs every day at 8:00 AM
    scheduler.add_job(
        func=send_festival_messages,
        args=[app],
        trigger='cron',
        hour=8,
        minute=0,
        id='festival_messages',
        replace_existing=True
    )

    scheduler.start()
    print("[Scheduler] Started ✅ — Appointment reminders every 1 hour, festival check daily at 8 AM.")
