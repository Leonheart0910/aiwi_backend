from pydantic import BaseModel, Field
from datetime import datetime

class CollectionSummaryOut(BaseModel):
    collection_id: int
    title: str = Field(alias="collection_title")
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }
