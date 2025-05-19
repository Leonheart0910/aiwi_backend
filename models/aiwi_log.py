from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from db.database import base

class AiwiLog(base):

    __tablename__ = "aiwi_log"

    chat_log_id = Column(Integer,primary_key=True, index=True)
    user_input = Column(String(255), nullable=False)
    ai_input1 = Column(String(255), nullable=False)
    ai_input2 = Column(String(255), nullable=False)
    ai_input3 = Column(String(255), nullable=False)
    aiwi_id = Column(Integer, ForeignKey("aiwi.aiwi_id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    aiwi = relationship("Aiwi", backref="aiwi_logs")


