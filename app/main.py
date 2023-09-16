from typing import List
from fastapi import Depends, FastAPI, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()  # fastapi instance

@app.get("/")  # GET operation on ROOT path/route -- this does the fastapi magic
def get_root():
    return {"Data": "hello world"}

# List as the response model as we return a list of PostResponse
@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # # Execute a query
    # cursor.execute("SELECT * FROM posts")

    # # Retrieve query results
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


# post_id is a path parameter
@app.get("/posts/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts where id = %s", [str(post_id)])
    # %s should match with string type -- so the conversion
    # the 2nd arg must be an iterable -- so we can choose to pass list, tuple anything
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    # filer ~ WHERE,fetchone ~ one(), we can use first to get the first match
    if post:
        return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No posts found with id : {post_id}",
    )


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
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
    return new_post


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    # cursor.execute("DELETE from posts WHERE id = %s returning *", [str(post_id)])
    # deleted_post = cursor.fetchone()
    deleted_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    db.delete(deleted_post)

    # conn.commit()
    db.commit()

    if deleted_post:
        return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No posts found with id : {post_id}",
    )


@app.put("/posts/{post_id}")
def update_post(
    post_id: int, post_update: schemas.PostUpdate, db: Session = Depends(get_db)
):
    # QUERY = (
    #     "UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *"
    # )
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    # cursor.execute(
    #     QUERY,
    #     (post_update.title, post_update.content, post_update.published, str(post_id)),
    # )
    # updated_post = cursor.fetchone()
    updated_post = post_query.first()
    post_query.update(post_update.model_dump())
    # conn.commit()
    db.commit()
    # for the RETURNING * part in SQL.
    db.refresh(updated_post)
    if updated_post:
        return updated_post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No posts found with id : {post_id}",
    )


@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_post(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**new_user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user