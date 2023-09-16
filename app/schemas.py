# schema of post
from pydantic import BaseModel


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
