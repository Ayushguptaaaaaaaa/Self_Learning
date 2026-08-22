# Query parameters & Path
from fastapi import FastAPI

app=FastAPI()

customer_risk_profile={
    101: {"name": "Ravi Kumar", "risk": "Low", "score": 0.12},
    102: {"name": "Priya Gupta",  "risk": "Medium", "score": 0.25},
    103: {"name":"Sneha Gupta", "risk": "High", "score": 0.5}
}

@app.get("/customer/{customer_id}")
def get_customer_risk(customer_id:int):
    if customer_id not in customer_risk_profile:
        return {"error":f"Cusotmer {customer_id} not found"}

    profile=customer_risk_profile[customer_id]
    return {
        "Customer_id": customer_id,
        "Name": profile["name"],
        "Risk_level": profile["risk"],
        "Score": profile["score"],
    }


@app.get("/model/{model_id}/customer/{customer_id}")
def get_model_prediction(model_name: str, customer_id: int):
    return {
        "Model_name": model_name, 
        "Customer_id": customer_id, 
        "Prediction": "High Risk"
    }