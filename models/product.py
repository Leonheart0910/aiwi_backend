from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import relationship

from db.database import base


class Product(base):

    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    item = relationship("Item", back_populates="products")
    product_info = relationship("ProductInfo", back_populates="product")
    image = relationship("Image", back_populates="product")
    ai_product = relationship("AiProduct", back_populates="ai_product")