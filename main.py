import random
from typing import Optional
from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()  # fastapi instance
# This is where we store our posts to memory
MY_POSTS = [
    {"id": 1, "title": "Title of post 1", "content": "Content of post1"},
    {"id": 2, "title": "Title of post 2", "content": "Content of post2"},
]


# schema of post
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # true is the default value
    rating: Optional[int] = None  # truly optional field


@app.get("/")  # GET operation on ROOT path/route -- this does the fastapi magic
def get_root():
    return {"Data": "hello world"}


@app.get("/posts")
def get_posts():
    return {"Data": MY_POSTS}


# post_id is a path parameter
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    for item in MY_POSTS:
        if item["id"] == post_id:
            return {"Data": item}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No posts found with id : {post_id}",
    )


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    post_dict = new_post.model_dump()  # convert the object to a dictionary
    # add random id to the entry -- not recommended
    post_dict["id"] = random.randint(0, 1000000)
    MY_POSTS.append(post_dict)  # adding post to memory
    return {"data": post_dict}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    for index in range(len(MY_POSTS)):
        if MY_POSTS[index]["id"] == post_id:
            del MY_POSTS[index]
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No posts found with id : {post_id}",
    )
