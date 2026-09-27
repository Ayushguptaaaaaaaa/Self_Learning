from fastapi import FastAPI, Depends,Header,HTTPException

app = FastAPI()

def varify_token(token: str = Header(None)):
    if token != "mysecrettoken":
        raise HTTPException(
            status_code=401,
            detail="Unauthorized"
        )
    return {
        "user":"Authorized User"
    }

@app.get("/secure-data")
def secure_data(user = Depends(varify_token)):
    return {
        "message":"Secure data accessed",
        "user":user
    }

# def common_logic():
#     return {
#         "message":"Common Logic executed"
#     }

# @app.get("/home")
# def home(data = Depends(common_logic)):
#     return data

# def get_current_user():
#     return{
#         "user":"Mohit"
#     }

# @app.get("/profile")
# def profile(user = Depends(get_current_user)):
#     return user

# @app.get("/dashboard")
# def dashboard(user = Depends(get_current_user)):
#     return user