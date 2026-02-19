# Campus Service Hub

A simple production-style campus portal built with FastAPI + SQLite + HTML/CSS/Vanilla JS.

Features:
- Authentication (admin / student / staff) with JWT
- Complaint management with optional image upload
- Event creation and student registration (capacity enforced)
- Room / lab booking with overlap checks and admin approval
- Announcements board
- Admin dashboard with counts and recent activity

Tech: FastAPI, SQLAlchemy, SQLite, Jinja2 templates, Vanilla JS

Quick start (SQLite)

1. No DB server required — SQLite file will be created automatically.
   - Optionally create schema manually: sqlite3 chattan.db < schema.sql

2. (Optional) Set DATABASE_URL environment variable. Default used when not set:
   sqlite:///./chattan.db

   Example for bash:
   export DATABASE_URL="sqlite:///./chattan.db"

3. Create a virtualenv and install deps:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

4. Run the app:
   uvicorn app.main:app --reload

5. Open http://127.0.0.1:8000

Default sample admin (auto-created on first run):
- email: admin@example.com
- password: admin123

Notes / configuration
- Change `SECRET_KEY` by setting the environment variable `SECRET_KEY`.
- File uploads are stored at `app/static/uploads/`.
- The project uses JWTs stored in localStorage for simplicity; for production use secure, HttpOnly cookies.

Structure
- `app/` - application package
  - `routers/`, `models/`, `schemas/`, `services/`, `templates/`, `static/`
- `schema.sql` - optional schema for SQLite (SQLAlchemy will create tables automatically)

This project is intentionally simple and educational — suitable for a final-year CS project.
