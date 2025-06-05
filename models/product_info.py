from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime, func
from sqlalchemy.orm import relationship

from database import Base


class ProductInfo(Base):

    __tablename__ = "product_info"
    product_info_id = Column(Integer, primary_key=True, nullable=False)
    product_id = Column(Integer, ForeignKey("product.product_id"),nullable=False)
    product_name = Column(String(255), nullable=False)
    product_link = Column(String(255), nullable=False)
    product_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    product = relationship("Product", backref="product_info")