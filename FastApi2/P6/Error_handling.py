from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class MarksSubmission(BaseModel):
    student_id: str
    marks: int
    subject: str

students = {
    "S001": {"name": "Ravi", "marks": 85, "grade": "A"},
    "S002": {"name": "Priya", "marks": 72, "grade": "B"},
    "S003": {"name": "Arjun", "marks": 91, "grade": "A+"}
}

@app.get("/student/{student_id}")
def get_student(student_id: str):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {student_id} not found"
        )

    return students[student_id]


@app.post("/submit-marks")
def submit_marks(submission: MarksSubmission):
    # error 1 students does not exists
    if submission.student_id not in students:
        raise HTTPException(
            status_code=404,
            detail=f"student with ID {submission.student_id} does not exists"
        )

    # error2 valid range 0 - 100
    if submission.marks < 0 or submission.marks > 100:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "marks must be between 0 and 100",
                "marks_received": submission.marks,
                "fix": "enter a valid value between 0 and 100"
            }
        )

    # error3 subject name cannot be empty
    if submission.subject.strip() == "":
        raise HTTPException(
            status_code=400,
            detail="subject name cannot be empty"
        )

    students[submission.student_id]["marks"] = submission.marks

    return {
        "message": "marks submitted successfully",
        "student": students[submission.student_id]["name"],
        "subject": submission.subject,
        "marks": submission.marks
    }
    