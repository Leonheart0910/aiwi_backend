from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

from schemas.product import ProductInfo
from schemas.recommend import RecommendInfo


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

class AiwiLogHistory(BaseModel):
    chat_log_id: int
    user_input: str
    keyword_text: str
    seo_keyword_text:str
    products: List[ProductInfo]
    recommend: List[RecommendInfo]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True
