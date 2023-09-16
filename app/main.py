from fastapi import Depends, FastAPI
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()  # fastapi instance
app.include_router(post.router) # adding router to app object
app.include_router(user.router) # adding router to app object

@app.get("/")  # GET operation on ROOT path/route -- this does the fastapi magic
def get_root():
    return {"Data": "hello world"}