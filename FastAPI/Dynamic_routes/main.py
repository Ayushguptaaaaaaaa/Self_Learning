from fastapi import FastAPI

app = FastAPI()

#Users Route
@app.get("/users/{user_id}")
def get_user(user_id:str):
    return {"user_id": user_id}