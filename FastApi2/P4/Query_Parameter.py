from fastapi import FastAPI

app=FastAPI()

all_customers= [
    {"id": 101, "name": "Ravi", "city": "Bengaluru", "risk": "low"},
    {"id": 102, "name": "Ramesh", "city": "Kolkata", "risk": "medium"},
    {"id": 103, "name": "Suresh", "city": "Mumbai", "risk": "high"},
    {"id": 104, "name": "Santosh", "city": "Pune", "risk": "low"},
    {"id": 105, "name": "Amit", "city": "Bangalore", "risk": "medium"}
]

@app.get("/customers")
def get_customers(city: str, risk: str):
    filtered= [
       c for c in all_customers
       if c["city"]==city and c["risk"]==risk
    ]

    return {
        "city":city,"risk":risk, "count": len(filtered), "customers":filtered
    }