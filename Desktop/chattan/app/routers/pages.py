from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get('/api/home/summary')
def home_summary(db: Session = Depends(get_db)):
    # announcements (latest 3)
    from app import models
    anns = db.query(models.Announcement).order_by(models.Announcement.created_at.desc()).limit(3).all()
    events = db.query(models.Event).order_by(models.Event.date.asc()).limit(3).all()
    stats = {
        'users': db.query(models.User).count(),
        'complaints': db.query(models.Complaint).count(),
        'events': db.query(models.Event).count(),
        'bookings': db.query(models.Booking).count(),
    }
    return {'announcements': [ { 'id': a.id, 'title': a.title, 'content': a.content, 'created_at': a.created_at } for a in anns ], 'events': [ { 'id': e.id, 'title': e.title, 'date': e.date, 'venue': e.venue } for e in events ], 'stats': stats }


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.get("/complaints")
def complaints_page(request: Request):
    return templates.TemplateResponse("complaints.html", {"request": request})


@router.get("/events")
def events_page(request: Request):
    return templates.TemplateResponse("events.html", {"request": request})


@router.get("/bookings")
def bookings_page(request: Request):
    return templates.TemplateResponse("bookings.html", {"request": request})


@router.get("/announcements")
def announcements_page(request: Request):
    return templates.TemplateResponse("announcements.html", {"request": request})


@router.get("/admin/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
