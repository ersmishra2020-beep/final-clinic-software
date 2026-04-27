if __name__ == "__main__":
    from scheduler import start_scheduler
    start_scheduler(app)
    app.run(host="0.0.0.0", port=5000)
from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask, render_template
from models import db
from routes import api
from scheduler import start_scheduler
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    # ─── Config ──────────────────────────────────────────────
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clinic_default_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///clinic.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ─── Database ────────────────────────────────────────────
    db.init_app(app)

    # ─── Routes ──────────────────────────────────────────────
    app.register_blueprint(api, url_prefix='/api')

    @app.route('/')
    def index():
        return render_template('index.html')

    # ─── Create tables ───────────────────────────────────────
    with app.app_context():
        db.create_all()
        seed_sample_data(app)

    # ─── Start background scheduler ──────────────────────────
    start_scheduler(app)

    return app


def seed_sample_data(app):
    """Add a sample doctor if none exist."""
    from models import Doctor
    if Doctor.query.count() == 0:
        doctors = [
            Doctor(name='Sharma', specialization='General Physician'),
            Doctor(name='Patel', specialization='Cardiologist'),
            Doctor(name='Gupta', specialization='Dermatologist'),
        ]
        db.session.add_all(doctors)
        db.session.commit()
        print("[Setup] Sample doctors added.")


if __name__ == '__main__':
    app = create_app()
    print("\n✅ Clinic System Running!")
    print("   Open: http://localhost:5000\n")
    app.run(debug=True, use_reloader=False)
