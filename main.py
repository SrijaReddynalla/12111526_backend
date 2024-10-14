from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Create a new task
@app.post("/v1/tasks", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(title=task.title, is_completed=task.is_completed)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# List all tasks
@app.get("/v1/tasks", response_model=List[schemas.TaskOut], status_code=status.HTTP_200_OK)
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    return tasks

# Get a specific task
@app.get("/v1/tasks/{id}", response_model=schemas.TaskOut, status_code=status.HTTP_200_OK)
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Edit a task
@app.put("/v1/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_task(id: int, updated_task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = updated_task.title
    task.is_completed = updated_task.is_completed
    db.commit()
    return

# Delete a specific task
@app.delete("/v1/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == id).first()
    if task:
        db.delete(task)
        db.commit()
    return

# Bulk add tasks
@app.post("/v1/tasks/bulk", status_code=status.HTTP_201_CREATED)
def bulk_add_tasks(tasks: schemas.BulkTaskCreate, db: Session = Depends(get_db)):
    new_tasks = [models.Task(title=task.title, is_completed=task.is_completed) for task in tasks.tasks]
    db.bulk_save_objects(new_tasks)
    db.commit()
    return {"tasks": [{"id": task.id} for task in new_tasks]}

# Bulk delete tasks
@app.delete("/v1/tasks/bulk", status_code=status.HTTP_204_NO_CONTENT)
def bulk_delete_tasks(task_ids: schemas.BulkTaskDelete, db: Session = Depends(get_db)):
    db.query(models.Task).filter(models.Task.id.in_(task_ids.tasks)).delete(synchronize_session=False)
    db.commit()
    return
