from fastapi import FastAPI, Body

app = FastAPI() #fastapi instance

@app.get("/")   # GET operation on ROOT path/route -- this does the fastapi magic
def get_root(): 
    return {"Data" : "hello world"}

@app.get("/posts")
def get_posts():
    return {"Data" : "Get Posts"}

@app.post("/create-post")
def create_post(payload : dict = Body(...)):
    return {"New Post" : f"Title : {payload['title']} Content: {payload['content']}"}