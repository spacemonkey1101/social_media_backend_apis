# schema of post
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # true is the default value
    # rating: Optional[int] = None  # truly optional field
