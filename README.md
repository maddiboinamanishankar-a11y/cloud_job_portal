# ☁️ Cloud-Based Job Portal

A full-stack Flask job portal that connects job seekers and employers.

## 🚀 Live Website

Add your deployed Render URL here:

`https://your-project.onrender.com`

## ✨ Features

### Job Seekers
- Register and login
- Browse and search jobs
- Filter jobs by location
- View job details
- Apply for jobs
- Track application status

### Employers
- Register and login as employer
- Post jobs
- View posted jobs
- View applicants
- Update application status
- Delete job postings

## 🛠️ Technology Stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML5
- CSS3
- Jinja2
- Gunicorn
- Render
- GitHub

## ▶️ Run Locally

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start:

```bash
python run.py
```

Open:

`http://127.0.0.1:5000`

## ☁️ Deploy on Render

- Connect your GitHub repository.
- Runtime: Python 3.
- Root Directory: leave empty if these files are at repository root.
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn run:app`

## Demo Employer

Email: `demo.employer@jobportal.com`

Password: `Demo@123`

Change the demo credentials before using this project publicly.
