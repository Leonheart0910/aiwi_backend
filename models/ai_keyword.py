from sqlalchemy import Column, Integer, ForeignKey, String, SmallInteger, DateTime, func
from sqlalchemy.orm import relationship

from database import Base


class AiKeyword(Base):

    __tablename__ = "ai_keyword"
    ai_keyword_id = Column(Integer, primary_key=True, nullable=False)
    chat_log_id = Column(Integer, ForeignKey("chat_log.chat_log_id"), nullable=False)
    keyword = Column(String(255), nullable=False)
    rank = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    chat_log = relationship("Chat_log", backref="ai_keyword")
