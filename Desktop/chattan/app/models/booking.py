from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, Time, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_name = Column(String(100))
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
