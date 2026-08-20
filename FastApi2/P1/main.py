from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"Message": "FastAPI is working!"}

@app.get("/about")
def about():
    return {"Project": "Loan Risk Model", "Version": "1.0"}