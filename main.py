from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import db, User, Job, Application
from functools import wraps
from sqlalchemy import or_

main_bp = Blueprint("main", __name__)

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped

def employer_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("auth.login"))
        if session.get("role") != "employer":
            flash("Employer access required.", "error")
            return redirect(url_for("main.dashboard"))
        return view(*args, **kwargs)
    return wrapped

@main_bp.route("/")
def index():
    q = request.args.get("q", "").strip()
    location = request.args.get("location", "").strip()
    query = Job.query
    if q:
        like = f"%{q}%"
        query = query.filter(or_(Job.title.ilike(like), Job.company.ilike(like), Job.skills.ilike(like)))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    jobs = query.order_by(Job.created_at.desc()).all()
    return render_template("index.html", jobs=jobs, q=q, location=location)

@main_bp.route("/dashboard")
@login_required
def dashboard():
    user = User.query.get(session["user_id"])
    if user.role == "employer":
        jobs = Job.query.filter_by(employer_id=user.id).order_by(Job.created_at.desc()).all()
        return render_template("employer_dashboard.html", user=user, jobs=jobs)
    applications = Application.query.filter_by(applicant_id=user.id).order_by(Application.created_at.desc()).all()
    return render_template("dashboard.html", user=user, applications=applications)

@main_bp.route("/job/<int:job_id>")
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    applied = False
    if "user_id" in session:
        applied = Application.query.filter_by(job_id=job.id, applicant_id=session["user_id"]).first() is not None
    return render_template("job_detail.html", job=job, applied=applied)

@main_bp.route("/job/<int:job_id>/apply", methods=["POST"])
@login_required
def apply(job_id):
    if session.get("role") != "jobseeker":
        flash("Only job seekers can apply for jobs.", "error")
        return redirect(url_for("main.job_detail", job_id=job_id))
    job = Job.query.get_or_404(job_id)
    existing = Application.query.filter_by(job_id=job.id, applicant_id=session["user_id"]).first()
    if existing:
        flash("You have already applied for this job.", "error")
        return redirect(url_for("main.job_detail", job_id=job_id))

    app = Application(
        job_id=job.id,
        applicant_id=session["user_id"],
        resume=request.form.get("resume", "").strip(),
        cover_letter=request.form.get("cover_letter", "").strip()
    )
    db.session.add(app)
    db.session.commit()
    flash("Application submitted successfully.", "success")
    return redirect(url_for("main.dashboard"))

@main_bp.route("/post-job", methods=["GET", "POST"])
@employer_required
def post_job():
    if request.method == "POST":
        required = ["title", "company", "location", "description"]
        if any(not request.form.get(x, "").strip() for x in required):
            flash("Please complete all required fields.", "error")
            return redirect(url_for("main.post_job"))

        job = Job(
            title=request.form["title"].strip(),
            company=request.form["company"].strip(),
            location=request.form["location"].strip(),
            job_type=request.form.get("job_type", "Full Time"),
            salary=request.form.get("salary", "").strip(),
            description=request.form["description"].strip(),
            skills=request.form.get("skills", "").strip(),
            employer_id=session["user_id"]
        )
        db.session.add(job)
        db.session.commit()
        flash("Job posted successfully.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("post_job.html")

@main_bp.route("/job/<int:job_id>/delete", methods=["POST"])
@employer_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    if job.employer_id != session["user_id"]:
        flash("You cannot delete this job.", "error")
        return redirect(url_for("main.dashboard"))
    db.session.delete(job)
    db.session.commit()
    flash("Job deleted.", "success")
    return redirect(url_for("main.dashboard"))

@main_bp.route("/applications/<int:job_id>")
@employer_required
def applications(job_id):
    job = Job.query.get_or_404(job_id)
    if job.employer_id != session["user_id"]:
        flash("Access denied.", "error")
        return redirect(url_for("main.dashboard"))
    apps = Application.query.filter_by(job_id=job.id).order_by(Application.created_at.desc()).all()
    return render_template("applications.html", job=job, applications=apps)

@main_bp.route("/application/<int:app_id>/status", methods=["POST"])
@employer_required
def update_status(app_id):
    application = Application.query.get_or_404(app_id)
    if application.job.employer_id != session["user_id"]:
        flash("Access denied.", "error")
        return redirect(url_for("main.dashboard"))
    status = request.form.get("status", "Applied")
    if status in ("Applied", "Shortlisted", "Interview", "Selected", "Rejected"):
        application.status = status
        db.session.commit()
    return redirect(url_for("main.applications", job_id=application.job_id))
