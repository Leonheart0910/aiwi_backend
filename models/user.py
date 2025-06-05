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

    user_info = relationship("UserInfo", backref="user", uselist=False, cascade="all, delete-orphan")
    collections = relationship("Collection", backref="user")
    aiwis = relationship("Aiwi", backref="user")
