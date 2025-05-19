from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from db.database import base

class UserInfo(base):
    __tablename__ = "user_info"

    user_info_id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=False)
    sex = Column(String(10), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="user_info")
