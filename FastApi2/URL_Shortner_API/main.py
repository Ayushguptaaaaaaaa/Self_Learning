from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import random, string 
from datetime import datetime

app = FastAPI()

BASE_URL = "http://localhost:8000"

url_storage={}

class URLRequest(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    short_code: str
    short_url: str 

class StatsResponse(BaseModel):
    url: str
    clicks: int
    created_at: str

def generate_short_code():
    while True:
        code=''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if code not in url_storage:
            return code

        
@app.post("/shorten", response_model=URLResponse, status_code=201)
def shorten_url(request: URLRequest):
    short_code = generate_short_code()
    created_at=datetime.now().isoformat()

    url_storage[short_code]= {
        "url": str(request.url),
        "clicks": 0,
        "created_at": created_at
    }

    short_url=f"{BASE_URL}/{short_code}"

    return {
        "short_code": short_code,
        "short_url": short_url
    }

@app.get("/stats/{short_code}", response_model=StatsResponse)
def get_stats(short_code: str):

    if short_code not in url_storage:
        raise HTTPException(status_code=404, detail="Short Code Not Found")

    return url_storage[short_code]

@app.get("/debug/storage")
def debug_storage():
    return {"storage": url_storage, "count": len(url_storage)}

@app.get("/{short_code}")
def redirect_url(short_code: str):
    print(f"Redirect called with: {short_code}")
    print(f"Storage keys: {list(url_storage.keys())}")
    print(f"Code in storage: {short_code in url_storage}")

    if short_code not in url_storage:
        raise HTTPException(status_code=404, detail="Short Code Not Found")

    url_storage[short_code]["clicks"]+=1
    original_url=url_storage[short_code]["url"]
    return RedirectResponse(url=original_url, status_code=302)



