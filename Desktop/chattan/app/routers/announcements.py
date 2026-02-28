from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import services, schemas
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/announcements", tags=["announcements"])


@router.post("/", status_code=201)
def create(title: str = Form(...), content: str = Form(...), attachment: str = Form(None), db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin only")
    a = services.announcement_service.create_announcement(db, title, content, user.id, attachment=attachment)
    return {"announcement": schemas.announcement.AnnouncementOut.from_orm(a)}


@router.get("/", response_model=List[schemas.announcement.AnnouncementOut])
def list_all(db: Session = Depends(get_db)):
    return services.announcement_service.list_announcements(db)


@router.delete("/{ann_id}")
def delete_announcement(ann_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin only")
    ok = services.announcement_service.delete_announcement(db, ann_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return {"ok": True}
