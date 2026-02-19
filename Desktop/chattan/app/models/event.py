from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    description = Column(Text)
    date = Column(DateTime)
    venue = Column(String(200))
    capacity = Column(Integer)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    registrations = relationship("EventRegistration", back_populates="event")
