from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app import services, schemas, models
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


@router.post("/", status_code=201)
def request_booking(payload: schemas.booking.BookingCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    # only students may request bookings
    if user.role != 'student':
        raise HTTPException(status_code=403, detail="Only students can request bookings")
    # prevent overlapping with approved bookings
    b = services.booking_service.create_booking(db, user.id, payload.room_name, payload.date, payload.start_time, payload.end_time)
    if not b:
        raise HTTPException(status_code=400, detail="Booking overlaps with existing approved booking")
    return {"booking": schemas.booking.BookingOut.from_orm(b)}


@router.get("/me", response_model=List[schemas.booking.BookingOut])
def my_bookings(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return services.booking_service.list_user_bookings(db, user.id)


@router.get("/", response_model=List[schemas.booking.BookingOut])
def all_bookings(db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin only")
    return services.booking_service.list_all_bookings(db)


@router.put("/{booking_id}/status")
def change_status(booking_id: int, status: str, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin only")
    b = services.booking_service.update_booking_status(db, booking_id, status)
    if not b:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"booking": schemas.booking.BookingOut.from_orm(b)}
