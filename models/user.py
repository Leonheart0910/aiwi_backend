from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from db.database import base

class User(base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    nickname = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user_info = relationship("UserInfo", back_populates="user", uselist=False, cascade="all, delete-orphan")
    collections = relationship("Collection", back_populates="user", cascade="all, delete-orphan")
    aiwi = relationship("Aiwi", back_populates="user", cascade="all, delete-orphan")
