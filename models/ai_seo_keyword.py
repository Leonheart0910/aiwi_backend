from sqlalchemy import Column, Integer, ForeignKey, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import SmallInteger, DateTime

from database import Base


class AiSeoKeyword(Base):

    __tablename__ = "ai_seo_keyword"

    ai_seo_keyword_id = Column(Integer, primary_key=True, nullable=False)
    chat_id_log = Column(Integer, ForeignKey("chat_log.chat_log_id"), nullable=False)
    seo_keyword = Column(String(255), nullable=False)
    rank = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    chat_log = relationship("Chat_log", backref="ai_seo_keyword")



