from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ComplaintCreate(BaseModel):
    title: str
    description: str
    category: str


class ComplaintOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    category: str
    status: str
    assigned_to: Optional[int]
    image_path: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
