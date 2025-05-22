from datetime import datetime

from pydantic import BaseModel

class UserInfoCreate(BaseModel):
    age: int
    sex: str


class UserInfoOut(BaseModel):
    user_info_id: int
    age: int
    sex: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True