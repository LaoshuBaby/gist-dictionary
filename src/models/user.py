from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
import uuid


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


class UserInDB(UserBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class User(UserInDB):
    pass


class UserList(BaseModel):
    users: List[User]
    total: int
    page: int
    limit: int