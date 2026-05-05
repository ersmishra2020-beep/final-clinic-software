from flask import Blueprint, request, jsonify
from models import db, Patient, Doctor, Appointment, FestivalMessage
from whatsapp_utils import send_whatsapp, appointment_confirmation_msg, appointment_cancelled_msg
from datetime import datetime

api = Blueprint('api', __name__)

# ─── PATIENTS ─────────────────────────────────────────

@api.route('/patients', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'phone': p.phone,
        'age': p.age,
        'address': p.address
    } for p in patients])


@api.route('/patients', methods=['POST'])
def add_patient():
    data = request.json

    if not data.get('name') or not data.get('phone'):
        return jsonify({'error': 'Name and phone required'}), 400

    if not data['phone'].startswith('+'):
        return jsonify({'error': 'Phone must include +91 format'}), 400

    patient = Patient(
        name=data['name'],
        phone=data['phone'],
        age=data.get('age'),
        address=data.get('address')
    )

    db.session.add(patient)
    db.session.commit()

    return jsonify({'message': 'Patient added', 'id': patient.id}), 201


# ─── DOCTORS ─────────────────────────────────────────

@api.route('/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'specialization': d.specialization
    } for d in doctors])


@api.route('/doctors', methods=['POST'])
def add_doctor():
    data = request.json

    doctor = Doctor(
        name=data['name'],
        specialization=data.get('specialization', '')
    )

    db.session.add(doctor)
    db.session.commit()

    return jsonify({'message': 'Doctor added', 'id': doctor.id}), 201


# ─── APPOINTMENTS ─────────────────────────────────────

@api.route('/appointments', methods=['POST'])
def book_appointment():
    data = request.json

    try:
        appt_date = datetime.strptime(data['appointment_date'], '%Y-%m-%dT%H:%M')
    except:
        return jsonify({'error': 'Invalid date format'}), 400

    patient = Patient.query.get(data['patient_id'])
    doctor = Doctor.query.get(data['doctor_id'])

    if not patient or not doctor:
        return jsonify({'error': 'Invalid patient/doctor'}), 404

    appt = Appointment(
        patient_id=patient.id,
        doctor_id=doctor.id,
        appointment_date=appt_date,
        status='scheduled'
    )

    db.session.add(appt)
    db.session.commit()

    # 📲 WhatsApp
    msg = appointment_confirmation_msg(patient.name, doctor.name, appt_date)
    send_whatsapp(patient.phone, msg)

    return jsonify({'message': 'Appointment booked'}), 201


@api.route('/appointments/<int:aid>/cancel', methods=['POST'])
def cancel_appointment(aid):
    appt = Appointment.query.get_or_404(aid)
    appt.status = 'cancelled'
    db.session.commit()

    msg = appointment_cancelled_msg(
        appt.patient.name,
        appt.doctor.name,
        appt.appointment_date
    )

    send_whatsapp(appt.patient.phone, msg)

    return jsonify({'message': 'Appointment cancelled'})


# ─── FESTIVAL ─────────────────────────────────────────

@api.route('/festivals', methods=['POST'])
def add_festival():
    data = request.json

    fdate = datetime.strptime(data['festival_date'], '%Y-%m-%d').date()

    festival = FestivalMessage(
        festival_name=data['festival_name'],
        festival_date=fdate,
        message_template=data['message_template']
    )

    db.session.add(festival)
    db.session.commit()

    return jsonify({'message': 'Festival saved'})
@api.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([{
        'id': a.id,
        'patient_name': a.patient.name,
        'doctor_name': a.doctor.name,
        'appointment_date': a.appointment_date.strftime('%Y-%m-%d %H:%M'),
        'status': a.status
    } for a in appointments])
@api.route('/festivals', methods=['GET'])
def get_festivals():
    festivals = FestivalMessage.query.all()
    return jsonify([{
        'id': f.id,
        'festival_name': f.festival_name,
        'festival_date': f.festival_date.strftime('%Y-%m-%d'),
        'message_template': f.message_template
    } for f in festivals])
@api.route('/festivals/<int:fid>/send-now', methods=['POST'])
def send_festival_now(fid):
    festival = FestivalMessage.query.get_or_404(fid)
    patients = Patient.query.all()

    for p in patients:
        msg = festival.message_template.replace("{name}", p.name)
        send_whatsapp(p.phone, msg)

    return jsonify({'message': 'Festival messages sent'})
@api.route('/appointments/<int:aid>/complete', methods=['POST'])
def complete_appointment(aid):
    appt = Appointment.query.get_or_404(aid)
    appt.status = 'completed'
    db.session.commit()

    return jsonify({'message': 'Appointment marked as completed'})