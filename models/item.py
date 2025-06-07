from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from db.database import base

class Item(base):
    __tablename__ = "item"

    item_id = Column(Integer, primary_key=True,index=True)
    collection_id = Column(Integer, ForeignKey("collection.collection_id"),unique=False, nullable=False)
    product_id = Column(Integer, ForeignKey("product.product_id"),unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    collection = relationship("Collection", back_populates="items")
    product = relationship("Product", back_populates="item")