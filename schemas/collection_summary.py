# schemas/collection_summary.py
from pydantic import BaseModel
from datetime import datetime

class CollectionSummaryOut(BaseModel):
    collection_id: int
    collection_title: str
    updated_at: datetime

    class Config:
        from_attributes = True
