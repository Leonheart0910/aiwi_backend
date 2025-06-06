from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime, func, BIGINT
from sqlalchemy.orm import relationship

from db.database import base


class ProductInfo(base):

    __tablename__ = "product_info"
    product_info_id = Column(Integer, primary_key=True, nullable=False)
    product_id = Column(BIGINT, ForeignKey("product.product_id"),nullable=False)
    product_name = Column(String(255), nullable=False)
    product_link = Column(String(255), nullable=False)
    product_price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    product = relationship("Product", back_populates="product_info")