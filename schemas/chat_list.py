from typing import List
from datetime import datetime
from pydantic import BaseModel

class ChatList(BaseModel):
    chat_id: str
    title: str
    updated_at: datetime