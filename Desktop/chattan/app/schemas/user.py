from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "student"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    phone: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]


class PasswordChange(BaseModel):
    old_password: str
    new_password: str
