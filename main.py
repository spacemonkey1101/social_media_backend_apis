from fastapi import FastAPI 

app = FastAPI() #fastapi instance

@app.get("/")   # GET operation on ROOT path/route -- this does the fastapi magic
def get_root(): 
    return {"Data" : "hello world"}

@app.get("/posts")
def get_posts():
    return {"Data" : "Get Posts"}