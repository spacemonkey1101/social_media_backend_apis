from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI() #fastapi instance

# schema of post
class Post(BaseModel):
    title : str
    content : str

@app.get("/")   # GET operation on ROOT path/route -- this does the fastapi magic
def get_root(): 
    return {"Data" : "hello world"}

@app.get("/posts")
def get_posts():
    return {"Data" : "Get Posts"}

@app.post("/create-post")
def create_post(new_post : Post ):
    return {"New Post" : f"Title : {new_post.title} Content: {new_post.content}"}