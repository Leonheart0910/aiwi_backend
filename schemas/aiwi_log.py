from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AiwiLogCreate(BaseModel):
    user_input: str
    ai_output1: str
    ai_output2: str
    ai_output3: str
    chat_id: int

class AiwiLogOut(BaseModel):
    chat_log_id: int
    user_input: str
    ai_input1: str
    ai_input2: str
    ai_input3: str
    chat_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True