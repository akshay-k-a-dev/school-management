import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base, SessionLocal
from app.routers import pages, auth, profile, complaints, events, bookings, announcements, dashboard
from app import models
from app.services import auth as auth_service

app = FastAPI(title="Campus Service Hub")

# Mount static files and include routers
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(complaints.router)
app.include_router(events.router)
app.include_router(bookings.router)
app.include_router(announcements.router)
app.include_router(dashboard.router)


@app.on_event("startup")
def startup_event():
    # create tables
    Base.metadata.create_all(bind=engine)

    # ensure `phone` column exists for older DBs (simple ALTER for SQLite)
    try:
        with engine.connect() as conn:
            if engine.dialect.name == 'sqlite':
                cols = [r[1] for r in conn.execute("PRAGMA table_info(users)")]
                if 'phone' not in cols:
                    conn.execute("ALTER TABLE users ADD COLUMN phone VARCHAR(32)")
            else:
                # other DBs: ignore (schema.sql updated)
                pass
    except Exception:
        pass

    # ensure sample admin exists
    db = SessionLocal()
    try:
        admin = db.query(models.User).filter_by(email='admin@example.com').first()
        if not admin:
            print('Creating sample admin account: admin@example.com / admin123')
            auth_service.create_user(db, 'Administrator', 'admin@example.com', 'admin123', role='admin')
    finally:
        db.close()
