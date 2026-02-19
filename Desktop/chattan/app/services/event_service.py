from sqlalchemy.orm import Session
from typing import List, Optional
from app import models
from datetime import datetime


def create_event(db: Session, title: str, description: str, date: datetime, venue: str, capacity: int, created_by: int):
    e = models.Event(
        title=title,
        description=description,
        date=date,
        venue=venue,
        capacity=capacity,
        created_by=created_by,
        created_at=datetime.utcnow(),
    )
    db.add(e)
    db.commit()
    db.refresh(e)
    return e


def list_events(db: Session) -> List[models.Event]:
    return db.query(models.Event).order_by(models.Event.date.asc()).all()


def get_event(db: Session, event_id: int) -> Optional[models.Event]:
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def count_registrations(db: Session, event_id: int) -> int:
    return db.query(models.EventRegistration).filter(models.EventRegistration.event_id == event_id).count()


def register_user_for_event(db: Session, event_id: int, user_id: int):
    # prevent duplicate
    exists = db.query(models.EventRegistration).filter(models.EventRegistration.event_id == event_id, models.EventRegistration.user_id == user_id).first()
    if exists:
        return exists
    reg = models.EventRegistration(event_id=event_id, user_id=user_id, registered_at=datetime.utcnow())
    db.add(reg)
    db.commit()
    db.refresh(reg)
    return reg


def unregister_user_from_event(db: Session, event_id: int, user_id: int):
    reg = db.query(models.EventRegistration).filter(models.EventRegistration.event_id == event_id, models.EventRegistration.user_id == user_id).first()
    if not reg:
        return None
    db.delete(reg)
    db.commit()
    return True


def list_event_participants(db: Session, event_id: int):
    return db.query(models.EventRegistration).filter(models.EventRegistration.event_id == event_id).all()
