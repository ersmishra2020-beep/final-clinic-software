from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# =========================
# PATIENT MODEL
# =========================
class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    phone = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
        index=True
    )  # Format: +919876543210

    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    address = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    appointments = db.relationship('Appointment', backref='patient', lazy=True)

    def __repr__(self):
        return f'<Patient {self.name}>'


# =========================
# DOCTOR MODEL
# =========================
class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    specialization = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    # Relationship
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def __repr__(self):
        return f'<Doctor {self.name}>'


# =========================
# APPOINTMENT MODEL
# =========================
class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey('patients.id'),
        nullable=False,
        index=True
    )

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey('doctors.id'),
        nullable=False,
        index=True
    )

    appointment_date = db.Column(
        db.DateTime,
        nullable=False,
        index=True
    )

    reason = db.Column(db.String(200))

    status = db.Column(
        db.String(20),
        default='scheduled'
    )
    # scheduled / completed / cancelled / no_show

    payment_status = db.Column(
        db.String(20),
        default='pending'
    )
    # pending / paid / failed

    cancel_reason = db.Column(db.String(200))

    reminder_sent = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f'<Appointment {self.id} - PatientID {self.patient_id}>'


# =========================
# FESTIVAL MESSAGE MODEL
# =========================
class FestivalMessage(db.Model):
    __tablename__ = 'festival_messages'

    id = db.Column(db.Integer, primary_key=True)

    festival_name = db.Column(db.String(100), nullable=False)
    festival_date = db.Column(db.Date, nullable=False)

    message_template = db.Column(db.Text, nullable=False)
    # Use {name} placeholder

    message_type = db.Column(db.String(20), default='whatsapp')
    # whatsapp / sms / email

    send_time = db.Column(db.DateTime)

    sent = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Festival {self.festival_name} on {self.festival_date}>'


# =========================
# NOTIFICATION LOG (IMPORTANT FOR WHATSAPP SYSTEM)
# =========================
class NotificationLog(db.Model):
    __tablename__ = 'notification_logs'

    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), index=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), index=True)

    message = db.Column(db.Text)
    status = db.Column(db.String(20))
    # sent / failed

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<NotificationLog {self.id} - {self.status}>'