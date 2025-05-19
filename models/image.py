from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from db.database import base

class Image(base):
    __tablename__ = "image"

    image_id = Column(Integer, primary_key=True, index=True)
    img_url = Column(String(255), nullable=False)
    item_id = Column(Integer, ForeignKey("item.item_id"),unique=False,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    item = relationship("Item", back_populates="images")