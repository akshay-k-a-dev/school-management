from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AnnouncementCreate(BaseModel):
    title: str
    content: str
    attachment: Optional[str] = None


class AnnouncementOut(BaseModel):
    id: int
    title: str
    content: str
    created_by: int
    created_at: datetime
    attachment: Optional[str]

    class Config:
        orm_mode = True
