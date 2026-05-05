import os
from flask import Flask, render_template
from models import db
from routes import api
from scheduler import start_scheduler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_app():
    app = Flask(__name__)

    # ─── Configuration ───────────────────────────────────────
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clinic_default_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'sqlite:///clinic.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ─── Initialize Extensions ───────────────────────────────
    db.init_app(app)

    # ─── Register Blueprints ─────────────────────────────────
    app.register_blueprint(api, url_prefix='/api')

    # ─── Routes ──────────────────────────────────────────────
    @app.route('/')
    def index():
        return render_template('index.html')

    # ─── Database Setup ──────────────────────────────────────
    with app.app_context():
        db.create_all()
        seed_sample_data()

    # ─── Scheduler (Safe for Production) ─────────────────────
    if os.environ.get("RENDER") != "true":
        start_scheduler(app)

    return app


def seed_sample_data():
    """Add sample doctors if database is empty."""
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


# ─── Local Development Entry Point ──────────────────────────
if __name__ == '__main__':
    app = create_app()
    print("\n✅ Clinic System Running!")
    print("   Open: http://localhost:5000\n")
    app.run(debug=False)