from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True # default value
#     # rating: Optional[int] = None # optional field that evaluate to None type

class UserBase(BaseModel):
    email : EmailStr

class UserCreate(UserBase):
    password : str


class User(UserBase):
    id : int
    created_at : datetime

    class Config:
        orm_mode = True

# class UserLogin(UserCreate):
#     pass

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    published: bool = True # default value
    # rating: Optional[int] = None # optional field that evaluate to None type

class Post(PostBase):
    id : int
    created_at: datetime
    user_id : int 
    user : User

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post : Post
    votes : int

    class Config:
        orm_mode = True


class Vote(BaseModel):
    post_id : int
    dir : conint(ge=0, le=1) # type: ignore