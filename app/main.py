import random
from typing import Optional
from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

while True:
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(
            "host=localhost dbname=social_media_db user=postgres password=password123",
            cursor_factory=RealDictCursor,
        )
        # Open a cursor to perform database operations
        cursor = conn.cursor()
        print("Database connection was successfull")
        break  # break out if we are able to establish a connection
    except Exception as e:
        print("Connecting to database failed with error : ", e)
        time.sleep(2)  # sleep for 2 seconds and then try again

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
    # rating: Optional[int] = None  # truly optional field


@app.get("/")  # GET operation on ROOT path/route -- this does the fastapi magic
def get_root():
    return {"Data": "hello world"}


@app.get("/posts")
def get_posts():
    # Execute a query
    cursor.execute("SELECT * FROM posts")

    # Retrieve query results
    posts = cursor.fetchall()
    return {"Data": posts}


# post_id is a path parameter
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    cursor.execute("SELECT * FROM posts where id = %s", [str(post_id)])
    # %s should match with string type -- so the conversion
    # the 2nd arg must be an iterable -- so we can choose to pass list, tuple anything
    post = cursor.fetchone()
    if post:
        return {"Data": post}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No posts found with id : {post_id}",
    )


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    # this is vulnerable to SQL injection
    # cursor.execute(f"INSERT INTO posts(title,content,published) VALUES ('{new_post.title}','{new_post.content}','{new_post.published}')")
    # cursor.execute does sanity check in the second arg for SQL attack
    cursor.execute(
        """INSERT INTO posts(title,content,published) VALUES (%s,%s,%s)
        RETURNING *""",
        (new_post.title, new_post.content, new_post.published),
    )
    new_post = cursor.fetchone()
    # to save changes to our db
    return {"data": new_post}


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


@app.put("/posts/{post_id}")
def delete_post(post_id: int, post_update: Post):
    for index in range(len(MY_POSTS)):
        if MY_POSTS[index]["id"] == post_id:
            post_dict = post_update.model_dump()
            post_dict["id"] = MY_POSTS[index]["id"]
            MY_POSTS[index] = post_dict
            return {"data": MY_POSTS[index]}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No posts found with id : {post_id}",
    )
