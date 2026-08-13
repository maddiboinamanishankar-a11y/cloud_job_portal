from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="jobseeker")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    jobs = db.relationship("Job", backref="employer", lazy=True)
    applications = db.relationship("Application", backref="applicant", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    company = db.Column(db.String(160), nullable=False)
    location = db.Column(db.String(160), nullable=False)
    job_type = db.Column(db.String(50), nullable=False, default="Full Time")
    salary = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.String(500))
    employer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("Application", backref="job", lazy=True, cascade="all, delete-orphan")

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    resume = db.Column(db.String(255))
    cover_letter = db.Column(db.Text)
    status = db.Column(db.String(40), default="Applied")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
