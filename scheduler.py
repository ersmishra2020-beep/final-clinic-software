if __name__ == "__main__":
    from scheduler import start_scheduler
    start_scheduler(app)
    app.run(debug=True, use_reloader=False)
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
        import pytz

        IST = pytz.timezone('Asia/Kolkata')
        now = datetime.now(IST)
        tomorrow = now + timedelta(hours=24)

        upcoming = Appointment.query.filter(
            Appointment.appointment_date >= now,
            Appointment.appointment_date <= tomorrow,
            Appointment.reminder_sent == False,
            Appointment.status == 'scheduled'
        ).all()

        print(f"[Scheduler] Checking reminders... Found {len(upcoming)} appointment(s).")

        for appt in upcoming:
            patient = appt.patient
            doctor = appt.doctor

            msg = appointment_reminder_msg(
                patient.name,
                doctor.name,
                appt.appointment_date
            )

            success = send_whatsapp(patient.phone, msg)

            if success:
                appt.reminder_sent = True
                print(f"[Scheduler] Reminder sent to {patient.name}")

        db.session.commit()   # ✅ commit once (better)


def send_festival_messages(app):
    """
    Runs every day at 8:00 AM.
    """
    with app.app_context():
        from models import db, FestivalMessage, Patient
        import pytz

        IST = pytz.timezone('Asia/Kolkata')
        today = datetime.now(IST).date()

        festivals = FestivalMessage.query.filter_by(
            festival_date=today,
            sent=False
        ).all()

        if not festivals:
            print(f"[Scheduler] No festival today ({today})")
            return

        patients = Patient.query.all()
        print(f"[Scheduler] Sending festival messages to {len(patients)} patients")

        for festival in festivals:
            for patient in patients:
                msg = festival.message_template.replace('{name}', patient.name)
                send_whatsapp(patient.phone, msg)

            festival.sent = True

        db.session.commit()   # ✅ commit once
        print("[Scheduler] Festival messages sent")


def start_scheduler(app):
    scheduler.add_job(
        func=send_appointment_reminders,
        args=[app],
        trigger='interval',
        hours=1,
        id='appointment_reminders',
        replace_existing=True
    )

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
    print("Scheduler started ✅")