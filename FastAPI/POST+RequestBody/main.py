from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int
    profession: str

# @app.post("/create-user")
# def create_user(name: str, age: int):
#     return {"name": name, "age": age}

@app.post("/create-user")
def create_user(user: User):
    return {
        "message": "User created successfully",
        "user": user
        }
