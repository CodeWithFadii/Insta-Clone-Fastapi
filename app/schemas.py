from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


# User schema ------------------


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserRegister(UserBase):
    pass


class UserLogin(UserBase):
    pass


class User(BaseModel):
    id: int
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}  # tells Pydantic to allow ORM objects


class UserOut(BaseModel):
    user: User


class UserAuthOut(BaseModel):
    access_token: str
    token_type: str
    user: User


# JWT Token schema------------------


class TokenData(BaseModel):
    id: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
