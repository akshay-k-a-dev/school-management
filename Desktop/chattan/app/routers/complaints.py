from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import os, shutil
from datetime import datetime

from app.database import get_db
from app import services, schemas, models
from app.routers.auth import get_current_user

router = APIRouter(prefix="/api/complaints", tags=["complaints"])

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
UPLOAD_DIR = os.path.abspath(UPLOAD_DIR)
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", status_code=201)
async def submit_complaint(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    # only students may submit complaints
    if user.role != 'student':
        raise HTTPException(status_code=403, detail="Only students can submit complaints")

    image_path = None
    if file:
        # basic validation: allow only common image types and limit size
        allowed = {"image/png", "image/jpeg", "image/jpg", "image/gif"}
        if file.content_type not in allowed:
            raise HTTPException(status_code=400, detail="Only image uploads are allowed")
        filename = os.path.basename(file.filename)
        filename = f"complaint_{int(datetime.utcnow().timestamp())}_{filename}"
        dest = os.path.join(UPLOAD_DIR, filename)
        # write in chunks and enforce max size (2MB)
        max_bytes = 2 * 1024 * 1024
        total = 0
        with open(dest, "wb") as buffer:
            while True:
                chunk = file.file.read(1024 * 64)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    buffer.close()
                    try:
                        os.remove(dest)
                    except Exception:
                        pass
                    raise HTTPException(status_code=400, detail="File too large (max 2MB)")
                buffer.write(chunk)
        image_path = f"/static/uploads/{filename}"

    c = services.complaint_service.create_complaint(db, user.id, title, description, category, image_path=image_path)
    return {"complaint": schemas.complaint.ComplaintOut.from_orm(c)}


@router.get("/me", response_model=List[schemas.complaint.ComplaintOut])
def my_complaints(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return services.complaint_service.list_user_complaints(db, user.id)


@router.get("/", response_model=List[schemas.complaint.ComplaintOut])
def list_all(db: Session = Depends(get_db), user = Depends(get_current_user)):
    # admin only
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin only")
    return services.complaint_service.list_all_complaints(db)


@router.put("/{complaint_id}/status")
def update_status(complaint_id: int, status: str = Form(...), assigned_to: int = Form(None), db: Session = Depends(get_db), user = Depends(get_current_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin only")
    updated = services.complaint_service.update_complaint_status(db, complaint_id, status, assigned_to)
    if not updated:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return {"complaint": schemas.complaint.ComplaintOut.from_orm(updated)}
