from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from db.database import base

class Image(base):
    __tablename__ = "images"

    image_id = Column(Integer, primary_key=True, index=True)
    img_url = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey("product.product_id"),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    product = relationship("Product", back_populates="image")