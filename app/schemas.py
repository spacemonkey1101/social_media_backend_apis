# schema of post
from typing import Optional
from pydantic import BaseModel, EmailStr


# user sending data to us
class PostBase(BaseModel):
    title: str
    content: str
    published: bool


class PostCreate(PostBase):
    published: bool = True


class PostUpdate(PostBase):
    pass  # accept whatever is extended


# us sending data to user
# we wont send back ID or created at like we did as this is private info and not useful to the user
class PostResponse(PostBase):
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

class Token(BaseModel):
    access_token : str
    token_type : str 
    
class TokenData(BaseModel):
    user_id : Optional[int] = None