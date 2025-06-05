from pydantic import BaseModel


class RecommendInfo(BaseModel):
    recommend_id: int
    recommend_text: str
    rank: int

    class Config:
        from_attributes = True