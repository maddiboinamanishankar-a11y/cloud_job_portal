from .models import db, User, Job

def seed_jobs():
    if Job.query.count() > 0:
        return
    employer = User.query.filter_by(email="demo.employer@jobportal.com").first()
    if not employer:
        employer = User(
            name="Demo Employer",
            email="demo.employer@jobportal.com",
            role="employer"
        )
        employer.set_password("Demo@123")
        db.session.add(employer)
        db.session.commit()

    jobs = [
        Job(
            title="Python Flask Developer",
            company="TechNova Solutions",
            location="Bengaluru, India",
            job_type="Full Time",
            salary="₹5 - ₹9 LPA",
            description="Build and maintain web applications using Python and Flask. Work with REST APIs, databases and cloud deployment.",
            skills="Python, Flask, SQL, REST API, Git",
            employer_id=employer.id
        ),
        Job(
            title="Frontend Developer",
            company="CloudWorks",
            location="Hyderabad, India",
            job_type="Full Time",
            salary="₹4 - ₹8 LPA",
            description="Create responsive and accessible user interfaces using HTML, CSS and JavaScript.",
            skills="HTML, CSS, JavaScript, Responsive Design",
            employer_id=employer.id
        ),
        Job(
            title="Data Analyst Intern",
            company="DataSphere",
            location="Remote",
            job_type="Internship",
            salary="₹15,000/month",
            description="Analyze datasets, prepare reports and create useful dashboards for business teams.",
            skills="Python, Excel, SQL, Pandas, Power BI",
            employer_id=employer.id
        )
    ]
    db.session.add_all(jobs)
    db.session.commit()
