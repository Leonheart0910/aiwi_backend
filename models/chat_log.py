from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import base

class ChatLog(base):

    __tablename__ = "chat_log"

    chat_log_id = Column(Integer,primary_key=True, index=True)
    user_input = Column(Text, nullable=False)
    chat_id = Column(Integer, ForeignKey("aiwi.chat_id"), nullable=False)
    keyword_full_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    aiwi = relationship("Aiwi", backref="chat_logs")



