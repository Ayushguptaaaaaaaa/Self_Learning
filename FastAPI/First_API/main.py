from fastapi import FastAPI

app = FastAPI()

# Home route
@app.get("/")
def home():
    return {"message": "Hello this is FastAPI!"}

# About route
@app.get("/about")
def about():
    return {"message": "This is the about page of FastAPI!"}

# Users route
@app.get("/users")
def users():
    return {
        "users": ["Mohit", "Rohit", "Amit"]
    }
