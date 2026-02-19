from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class EventRegistration(Base):
    __tablename__ = "event_registrations"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    registered_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", back_populates="registrations")
    user = relationship("User", back_populates="registrations")
