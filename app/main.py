import random
from typing import Optional
from fastapi import Depends, FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

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

models.Base.metadata.create_all(bind=engine)

app = FastAPI()  # fastapi instance


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
def get_posts(db: Session = Depends(get_db)):
    # # Execute a query
    # cursor.execute("SELECT * FROM posts")

    # # Retrieve query results
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
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
def create_post(new_post: Post, db: Session = Depends(get_db)):
    # this is vulnerable to SQL injection
    # cursor.execute(f"INSERT INTO posts(title,content,published) VALUES ('{new_post.title}','{new_post.content}','{new_post.published}')")
    # cursor.execute does sanity check in the second arg for SQL attack
    # cursor.execute(
    #     """INSERT INTO posts(title,content,published) VALUES (%s,%s,%s)
    #     RETURNING *""",
    #     (new_post.title, new_post.content, new_post.published),
    # )
    new_post = models.Post(
        # title=new_post.title, content=new_post.content, published=new_post.published
        # More efficent way to do the above is to unpack a dict which gives the above output
        **new_post.model_dump()
    )
    # new_post = cursor.fetchone()
    db.add(new_post)
    # # to save changes to our db
    # conn.commit()
    db.commit()
    # for the RETURNING * part in SQL.
    db.refresh(new_post)
    return {"data": new_post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    cursor.execute("DELETE from posts WHERE id = %s returning *", [str(post_id)])
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post:
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No posts found with id : {post_id}",
    )


@app.put("/posts/{post_id}")
def update_post(post_id: int, post_update: Post):
    QUERY = (
        "UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *"
    )
    cursor.execute(
        QUERY,
        (post_update.title, post_update.content, post_update.published, str(post_id)),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post:
        return {"data": updated_post}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No posts found with id : {post_id}",
    )
