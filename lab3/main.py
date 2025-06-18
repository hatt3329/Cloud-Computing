from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
#pydantic will automatically vet incoming msgs for invalid inputs
from pydantic import BaseModel

app = FastAPI()

# Task layout
class Task(BaseModel):
    id: int
    title: str
    description: str = ""
    completed: bool = False

# task list
tasks: List[Task] = []

# HelloWorld
@app.get("/hello")
def hello():
    return {"message": "Hello Earth :)"}

# gathering all tasks
@app.get("/")
def get_tasks():
    return tasks

#new task
@app.post("/tasks")
def create_task(task: Task):
    for existing in tasks:
        if existing.id == task.id:
            raise HTTPException(status_code=400, detail="Task ID already exists")
    tasks.append(task)
    return task

# mark all complete
@app.put("/tasks/complete-all")
def mark_all_complete():
    for task in tasks:
        task.completed = True
    return {"message": "All tasks marked complete"}

# mark all tasks as incomplete
@app.put("/tasks/reset-all")
def reset_all_tasks():
    for task in tasks:
        task.completed = False
    return {"message": "All are now marked incomplete"}

# wipe all tasks
@app.put("/tasks/clear")
def clear_all_tasks(confirm: bool):
    if confirm:
        tasks.clear()
        return {"message": "All tasks wiped!"}
    raise HTTPException(status_code=400, detail="confirmation needed")

# completion status
@app.get("/tasks/status")
def get_tasks_by_status(completed: bool):
    return [task for task in tasks if task.completed == completed]

# query string search
@app.get("/tasks/search")
def search_tasks(title: str = Query(...)):
    return [task for task in tasks if title.lower() in task.title.lower()]

# Count of all tasks
@app.get("/tasks/count")
def task_count():
    return {"count": len(tasks)}

# Count completed tasks
@app.get("/tasks/count/completed")
def completed_task_count():
    return {"completed": len([task for task in tasks if task.completed])}

# getting task via ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# task updating
@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

# task deletion
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(i)
    raise HTTPException(status_code=404, detail="Task not found")

# Mark task complete using path param
@app.put("/tasks/{task_id}/complete")
def mark_task_complete(task_id: int):
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# Update title using query param
@app.put("/tasks/{task_id}/title")
def update_title(task_id: int, title: str):
    for task in tasks:
        if task.id == task_id:
            task.title = title
            return task
    raise HTTPException(status_code=404, detail="Task not found")

#update description
@app.put("/tasks/{task_id}/description")
def update_description(task_id: int, description: str):
    for task in tasks:
        if task.id == task_id:
            task.description = description
            return task
    raise HTTPException(status_code=404, detail="Task not found")
