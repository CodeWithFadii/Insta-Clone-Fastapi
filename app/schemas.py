from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


# User schema ------------------


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserRegister(UserBase):
    name: str
    pass


class UserLogin(UserBase):
    pass


class User(BaseModel):
    id: UUID
    email: str
    name: str
    user_name: Optional[str] = "null"
    profile_img: Optional[str] = "null"
    followers: int
    followings: int
    posts: int
    created_at: datetime

    model_config = {"from_attributes": True, "json_encoders": {UUID: lambda v: str(v)}}


class UserOut(BaseModel):
    user: User


class UserAuthOut(BaseModel):
    access_token: str
    token_type: str
    user: User


# JWT Token schema------------------


class TokenData(BaseModel):
    id: Optional[UUID] = None


class Token(BaseModel):
    access_token: str
    token_type: str


# Pagination schema------------------   


class PaginatedUsers(BaseModel):
    users: List[User]
    total_count: int
    next_cursor: Optional[UUID]
