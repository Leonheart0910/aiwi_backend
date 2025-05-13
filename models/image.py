from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Image(Base):
    __tablename__ = "image"

    image_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("item.id"),unique=False,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    item = relationship("Item", back_populates="images")