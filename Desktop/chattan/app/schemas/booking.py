from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional


class BookingCreate(BaseModel):
    room_name: str
    date: date
    start_time: time
    end_time: time


class BookingOut(BaseModel):
    id: int
    user_id: int
    room_name: str
    date: date
    start_time: time
    end_time: time
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
