from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LoanApplication(BaseModel):
    age: int
    income: float
    loan_amount: float
    employment_years:int

@app.post("/predict_loan_status")
def predict_loan(application: LoanApplication):
    if application.income>50000 and application.employment_years>=2:
        decision= "Approved"
    else:
        decision= "Rejected"

    return {"message": "Prediction Successful",
            "application_age": application.age,
            "Loan_Amount": application.loan_amount,
            "Loan Desision": decision }