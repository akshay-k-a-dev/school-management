from sqlalchemy.orm import Session
from app import models


def get_dashboard_stats(db: Session):
    users = db.query(models.User).count()
    complaints = db.query(models.Complaint).count()
    events = db.query(models.Event).count()
    bookings = db.query(models.Booking).count()
    return {
        "users": users,
        "complaints": complaints,
        "events": events,
        "bookings": bookings,
    }


def get_recent_activity(db: Session, limit: int = 10):
    # Simple combined recent items (complaints, events, bookings, announcements)
    recent_complaints = db.query(models.Complaint.id.label('id'), models.Complaint.title.label('title'), models.Complaint.created_at.label('created_at'), models.Complaint.status.label('type')).order_by(models.Complaint.created_at.desc()).limit(limit).all()
    recent_events = db.query(models.Event.id.label('id'), models.Event.title.label('title'), models.Event.created_at.label('created_at'), models.Event.venue.label('type')).order_by(models.Event.created_at.desc()).limit(limit).all()
    recent_bookings = db.query(models.Booking.id.label('id'), models.Booking.room_name.label('title'), models.Booking.created_at.label('created_at'), models.Booking.status.label('type')).order_by(models.Booking.created_at.desc()).limit(limit).all()
    recent_ann = db.query(models.Announcement.id.label('id'), models.Announcement.title.label('title'), models.Announcement.created_at.label('created_at'), models.Announcement.attachment.label('type')).order_by(models.Announcement.created_at.desc()).limit(limit).all()

    # Merge and sort by created_at locally
    combined = []
    for r in recent_complaints:
        combined.append({"kind": "complaint", "id": r.id, "title": r.title, "created_at": r.created_at})
    for r in recent_events:
        combined.append({"kind": "event", "id": r.id, "title": r.title, "created_at": r.created_at})
    for r in recent_bookings:
        combined.append({"kind": "booking", "id": r.id, "title": r.title, "created_at": r.created_at})
    for r in recent_ann:
        combined.append({"kind": "announcement", "id": r.id, "title": r.title, "created_at": r.created_at})

    combined_sorted = sorted(combined, key=lambda x: x["created_at"], reverse=True)
    return combined_sorted[:limit]
