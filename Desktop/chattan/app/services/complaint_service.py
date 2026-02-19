from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas
from datetime import datetime


def create_complaint(db: Session, user_id: int, title: str, description: str, category: str, image_path: Optional[str] = None):
    c = models.Complaint(
        user_id=user_id,
        title=title,
        description=description,
        category=category,
        image_path=image_path,
        created_at=datetime.utcnow(),
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


def list_user_complaints(db: Session, user_id: int) -> List[models.Complaint]:
    return db.query(models.Complaint).filter(models.Complaint.user_id == user_id).order_by(models.Complaint.created_at.desc()).all()


def list_all_complaints(db: Session) -> List[models.Complaint]:
    return db.query(models.Complaint).order_by(models.Complaint.created_at.desc()).all()


def update_complaint_status(db: Session, complaint_id: int, status: str, assigned_to: Optional[int] = None):
    c = db.query(models.Complaint).filter(models.Complaint.id == complaint_id).first()
    if not c:
        return None
    c.status = status
    if assigned_to:
        c.assigned_to = assigned_to
    db.commit()
    db.refresh(c)
    return c
