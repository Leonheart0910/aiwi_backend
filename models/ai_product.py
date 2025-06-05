from sqlalchemy import ForeignKey, Column, Integer, Numeric
from sqlalchemy.orm import relationship

from db.database import base


class AiProduct(base):
    __tablename__ = "ai_product"
    ai_product_id= Column(Integer, primary_key=True)
    ai_keyword_id = Column(Integer, ForeignKey("ai_keyword.ai_keyword_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.product_id"), nullable=False)
    rank = Column(Numeric(10,2), nullable=False)

    ai_keyword = relationship("AiKeyword", back_populates="ai_product")
    product = relationship("Product", back_populates="ai_product")
