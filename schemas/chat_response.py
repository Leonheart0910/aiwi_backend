from pydantic import BaseModel
from typing import List
from datetime import datetime


class ImageOut(BaseModel):
    image_id: int
    image_url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProductOut(BaseModel):
    product_id: int
    product_name: str
    product_link: str
    product_price: str
    rank: float
    image: ImageOut
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RecommendOut(BaseModel):
    recommend_id: int
    recommend_text: str
    rank: int

    class Config:
        from_attributes = True


class ChatLogOut(BaseModel):
    chat_log_id: int
    user_input: str
    keyword_text: str
    seo_keyword_text: str
    products: List[ProductOut]
    recommend: List[RecommendOut]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatOut(BaseModel):
    chat_id: str
    title: str
    chat_log: List[ChatLogOut]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
