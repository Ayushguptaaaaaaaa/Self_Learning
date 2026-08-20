from fastapi import FastAPI

app = FastAPI()

@app.get("/Users")
def users(name: str=None):
    return {"Name": name}

# Setting Default Value for Query Parameter
@app.get("/products")
def products(limit: int=10):
    return {"limit": limit}

# Multiple Query Parameters
@app.get("/items")
def items(name:str=None, price: int=0):
    return {"Name": name, "Price": price}