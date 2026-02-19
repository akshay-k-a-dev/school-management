from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    date: datetime
    venue: str
    capacity: int


class EventOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    date: datetime
    venue: str
    capacity: int
    created_by: int
    created_at: datetime

    class Config:
        orm_mode = True
