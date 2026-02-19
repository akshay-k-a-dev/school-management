from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.routers.auth import get_current_user
from app import services, models
from app.schemas.user import UserUpdate, PasswordChange, UserOut

router = APIRouter(prefix="/api/profile", tags=["profile"])


@router.get("/", response_model=UserOut)
def get_profile(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return user


@router.put("/")
def update_profile(payload: UserUpdate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    # allow updating name / email / phone
    if payload.email:
        # ensure unique
        existing = db.query(models.User).filter(models.User.email == payload.email).first()
        if existing and existing.id != user.id:
            raise HTTPException(status_code=400, detail="Email already in use")
        user.email = payload.email
    if payload.name is not None:
        user.name = payload.name
    if payload.phone is not None:
        user.phone = payload.phone
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"user": UserOut.from_orm(user)}


@router.post("/change-password")
def change_password(payload: PasswordChange, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if not services.auth.verify_password(payload.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    user.password_hash = services.auth.hash_password(payload.new_password)
    db.add(user)
    db.commit()
    return {"ok": True}


@router.get('/events')
def my_events(db: Session = Depends(get_db), user = Depends(get_current_user)):
    """Return upcoming and past events the user has registered for."""
    from datetime import datetime
    regs = db.query(models.Event).join(models.EventRegistration, models.Event.id == models.EventRegistration.event_id).filter(models.EventRegistration.user_id == user.id).order_by(models.Event.date.asc()).all()
    upcoming = []
    past = []
    now = datetime.utcnow()
    for e in regs:
        if e.date and e.date >= now:
            upcoming.append(e)
        else:
            past.append(e)
    return {"upcoming": [schemas.event.EventOut.from_orm(e) for e in upcoming], "past": [schemas.event.EventOut.from_orm(e) for e in past]}
