from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import services, schemas, models
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/events", tags=["events"])


@router.post("/", status_code=201)
def create_event(payload: schemas.event.EventCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin only")
    e = services.event_service.create_event(db, payload.title, payload.description, payload.date, payload.venue, payload.capacity, user.id)
    return {"event": schemas.event.EventOut.from_orm(e)}


@router.get("/", response_model=List[schemas.event.EventOut])
def list_events(db: Session = Depends(get_db)):
    return services.event_service.list_events(db)


@router.get('/registrations/me')
def my_event_registrations(db: Session = Depends(get_db), user = Depends(get_current_user)):
    """Return event IDs the current user is registered for."""
    regs = db.query(models.EventRegistration).filter(models.EventRegistration.user_id == user.id).all()
    return {"event_ids": [r.event_id for r in regs]}


@router.post("/{event_id}/register")
def register(event_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    event = services.event_service.get_event(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    count = services.event_service.count_registrations(db, event_id)
    if count >= event.capacity:
        raise HTTPException(status_code=400, detail="Event is full")
    reg = services.event_service.register_user_for_event(db, event_id, user.id)
    return {"registration_id": reg.id}


@router.post("/{event_id}/unregister")
def unregister(event_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    ok = services.event_service.unregister_user_from_event(db, event_id, user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Registration not found")
    return {"ok": True}


@router.get("/{event_id}/participants")
def participants(event_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin only")
    regs = services.event_service.list_event_participants(db, event_id)
    return {"participants": [r.user_id for r in regs]}
