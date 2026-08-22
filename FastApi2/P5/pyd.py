from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LoanApplication(BaseModel):
    name: str
    age: int
    income: float
    loan_amount: float
    employment_years:int


@app.post("/predict")
def predict_loan(loan_application:LoanApplication):
    approved=(
        loan_application.income>50000 and
        loan_application.age>=21 and 
        loan_application.employment_years>3
    )

    return {
        "applicant_name": loan_application.name,
        "applicant_age": loan_application.age,
        "loan_decision": "Approved" if approved else "Rejected",
        "applicant_income": loan_application.income,
        "loan_amount": loan_application.loan_amount,
        "employment_years": loan_application.employment_years
    }