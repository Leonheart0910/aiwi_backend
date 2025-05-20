from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import base

class AiwiLog(base):

    __tablename__ = "aiwi_log"

    chat_log_id = Column(Integer,primary_key=True, index=True)
    user_input = Column(String(255), nullable=False)
    ai_output1 = Column(Text, nullable=False)
    ai_output2 = Column(Text, nullable=False)
    ai_output3 = Column(Text, nullable=False)
    chat_id = Column(Integer, ForeignKey("aiwi.chat_id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    aiwi = relationship("Aiwi", backref="aiwi_logs")


