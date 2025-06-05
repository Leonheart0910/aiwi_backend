from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import relationship

from database import Base


class AiRecommend(Base):

    __tablename__ = "ai_recommend"
    ai_recommend_id = Column(Integer, primary_key=True)
    chat_log_id = Column(Integer, ForeignKey("chat_log.chat_log_id"), nullable=False)
    recommend = Column(Text, nullable=False)
    rank = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    chat_log = relationship("Chat_log", backref="ai_recommend")
