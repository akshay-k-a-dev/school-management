from sqlalchemy.orm import Session
from typing import List, Optional
from app import models
from datetime import datetime, time


def create_booking(db: Session, user_id: int, room_name: str, date, start_time: time, end_time: time):
    # check overlap with approved bookings
    overlapping = db.query(models.Booking).filter(
        models.Booking.room_name == room_name,
        models.Booking.date == date,
        models.Booking.status == 'approved',
        models.Booking.start_time < end_time,
        models.Booking.end_time > start_time,
    ).first()
    if overlapping:
        return None
    b = models.Booking(
        user_id=user_id,
        room_name=room_name,
        date=date,
        start_time=start_time,
        end_time=end_time,
        status='pending',
        created_at=datetime.utcnow(),
    )
    db.add(b)
    db.commit()
    db.refresh(b)
    return b


def list_user_bookings(db: Session, user_id: int) -> List[models.Booking]:
    return db.query(models.Booking).filter(models.Booking.user_id == user_id).order_by(models.Booking.date.desc(), models.Booking.start_time).all()


def list_all_bookings(db: Session) -> List[models.Booking]:
    return db.query(models.Booking).order_by(models.Booking.date.desc()).all()


def update_booking_status(db: Session, booking_id: int, status: str):
    b = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not b:
        return None
    b.status = status
    db.commit()
    db.refresh(b)
    return b
