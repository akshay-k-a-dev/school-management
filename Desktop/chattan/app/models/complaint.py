from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200))
    description = Column(Text)
    category = Column(String(100))
    status = Column(String(20), default="pending")
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    image_path = Column(String(256), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # the creator of the complaint
    user = relationship("User", foreign_keys=[user_id], back_populates="complaints")
    # staff member assigned to the complaint (optional)
    assigned = relationship("User", foreign_keys=[assigned_to], uselist=False)
