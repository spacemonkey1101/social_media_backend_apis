from fastapi import FastAPI 

app = FastAPI() #fastapi instance

@app.get("/")
def get_root():
    return {"Data" : "hello world"}