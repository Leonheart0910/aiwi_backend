from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Item(Base):
    __tablename__ = "item"

    item_id = Column(Integer, primary_key=True,index=True)
    category_name = Column(String(255), nullable=False)
    product_name = Column(String(255), nullable=False)
    img_url = Column(String(255), nullable=False)
    product_info = Column(String(255), nullable=False)
    collection_id = Column(Integer, ForeignKey("collection.id"),unique=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    image = relationship("Image", back_populates="item")
    collection = relationship("Collection", back_populates="items")