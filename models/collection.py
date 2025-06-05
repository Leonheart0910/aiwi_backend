from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from db.database import base

class Collection(base):
    __tablename__ = "collection"

    collection_id = Column(Integer, primary_key=True, index=True)
    collection_title = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    items = relationship("Item", backref="collection", cascade="all, delete-orphan")
    user = relationship("User", backref="collections")


