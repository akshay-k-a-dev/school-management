from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from app.database import Base


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    attachment = Column(String(256), nullable=True)
