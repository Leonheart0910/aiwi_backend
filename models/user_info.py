from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import base

class UserInfo(base):
    __tablename__ = "user_info"

    user_info_id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=False)
    sex = Column(String(10), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=True, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    user = relationship("User", back_populates="user_info")
