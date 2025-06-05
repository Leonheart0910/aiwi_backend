from sqlalchemy import Column, Integer, DateTime, func

from database import Base


class Product(Base):

    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

