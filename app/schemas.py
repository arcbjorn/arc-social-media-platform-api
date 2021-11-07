from pydantic import BaseModel
from datetime import datetime

from pydantic.networks import EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


# response Post model
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode: True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode: True


class UserLoginDto(BaseModel):
    email: EmailStr
    password: str
