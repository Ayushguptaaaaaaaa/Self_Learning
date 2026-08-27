from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import uuid
import asyncio
from datetime import datetime
from typing import Optional


app = FastAPI()

tasks_storage = {}

class TaskRequest(BaseModel):
    task_type: str  
    params: dict    


# Model for task status responses
class TaskResponse(BaseModel):
    task_id: str
    task_type: str
    status: str 
    params: dict
    result: Optional[str] = None  
    created_at: str
    completed_at: Optional[str] = None  


class TaskSubmitResponse(BaseModel):
    task_id: str
    status: str
    message: str  

# Step 3 — Background Task Worker Function

async def process_task(task_id: str):
    """Simulates the actual work being done in the background"""
    try:
        task = tasks_storage[task_id]

        task["status"] = "running"
        
        task_type = task["task_type"]

        if task_type == "send_email":
            await asyncio.sleep(5)
            task["result"] = "Email sent successfully"
            task["status"] = "completed"
        elif task_type == "generate_report":
            await asyncio.sleep(10)
            task["result"] = "Report generated successfully"
            task["status"] = "completed"
        elif task_type == "process_image":
            await asyncio.sleep(8)
            task["result"] = "Image processed successfully"
            task["status"] = "completed"
        else:
            task["status"] = "failed"
            task["result"] = "Unknown task type"

        task["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        task["status"] = "failed"
        task["result"] = f"Error: {str(e)}"
        task["completed_at"] = datetime.now().isoformat()




@app.post("/tasks", response_model=TaskSubmitResponse, status_code=202)
async def submit_task(request: TaskRequest, background_tasks: BackgroundTasks):
    """Accepts a task submission and runs it in the background"""
    
    task_id = str(uuid.uuid4())
    
    tasks_storage[task_id] = {
        "task_id": task_id,
        "task_type": request.task_type,
        "params": request.params,
        "status": "pending",
        "result": None,
        "created_at": datetime.now().isoformat(),
        "completed_at": None
    }
    
    background_tasks.add_task(process_task, task_id)
    
    return TaskSubmitResponse(
        task_id=task_id,
        status="pending",
        message="Task queued successfully"
    )



@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Returns the status and details of a specific task"""
    
    if task_id not in tasks_storage:
        raise HTTPException(
            status_code=404, 
            detail="Task not found"
            )
    
    return tasks_storage[task_id]



@app.get("/tasks", response_model=list[TaskResponse])
async def list_tasks(status: Optional[str] = None):
    """Lists all tasks, with optional filtering by status"""
    
    if status:
        return [task for task in tasks_storage.values() if task["status"] == status]
    
    return list(tasks_storage.values())



@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Deletes a task from storage"""
    
    if task_id not in tasks_storage:
        raise HTTPException(status_code=404, detail="Task not found")

    del tasks_storage[task_id]

    return {"message": "Task deleted successfully"}