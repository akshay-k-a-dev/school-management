from sqlalchemy.orm import Session
from typing import List
from app import models
from datetime import datetime


def create_announcement(db: Session, title: str, content: str, created_by: int, attachment: str = None):
    a = models.Announcement(title=title, content=content, created_by=created_by, attachment=attachment, created_at=datetime.utcnow())
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


def list_announcements(db: Session) -> List[models.Announcement]:
    return db.query(models.Announcement).order_by(models.Announcement.created_at.desc()).all()
