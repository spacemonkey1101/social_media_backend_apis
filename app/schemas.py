# schema of post
from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool


class PostCreate(PostBase):
    published: bool = True


class PostUpdate(PostBase):
    pass  # accept whatever is extended
