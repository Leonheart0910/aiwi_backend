from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from schemas.user_info import UserInfoCreate, UserInfoOut


class UserCreate(BaseModel):
    email: str
    nickname: str
    password: str
    user_info: Optional[UserInfoCreate] = None

class UserOut(BaseModel):
    user_id: int
    email: str
    nickname: str
    user_info: UserInfoOut
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserWithDrawRequest(BaseModel):
    user_id: int

class UserLoginResponse(BaseModel):
    user_id: int
    nickname: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class UserSignupRequest(BaseModel):
    email: str
    nickname: str
    password: str
    age: int
    sex: str

class UserInputRequest(BaseModel):
    aiwi_id: Optional[int] = None
    user_id: int
    query: str

class UserInformationResponse(BaseModel):
    user_id: int
    email: str
    password: str
    nickname: str
    user_info: UserInfoOut
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True