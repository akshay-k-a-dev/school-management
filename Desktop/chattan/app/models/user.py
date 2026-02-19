from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128))
    email = Column(String(128), unique=True, index=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(20), default="student", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    phone = Column(String(32), nullable=True)

    complaints = relationship("Complaint", back_populates="user", foreign_keys='Complaint.user_id')
    bookings = relationship("Booking", back_populates="user")
    registrations = relationship("EventRegistration", back_populates="user")
