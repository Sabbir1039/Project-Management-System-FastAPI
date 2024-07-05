from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud.task import create_task, get_project_tasks, get_task_by_id, update_task, delete_task
from ..schemas.task import TaskCreateSchema, TaskResponseSchema, TaskUpdateSchema
from ..database import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=TaskResponseSchema)
def create_task(task: TaskCreateSchema, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)  # Example with fixed project_id

# Get all tasks for a specific project
@router.get("/project/{project_id}", response_model=List[TaskResponseSchema])
def read_project_tasks(project_id: int, db: Session = Depends(get_db)):
    tasks = get_project_tasks(db, project_id)
    return tasks


# Get a specific task by its ID
@router.get("/{task_id}", response_model=TaskResponseSchema)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Update a task
@router.put("/{task_id}", response_model=TaskResponseSchema)
def update_existing_task(task_id: int, task_update: TaskUpdateSchema, db: Session = Depends(get_db)):
    updated_task = update_task(db, task_id, task_update)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

# Delete a task
@router.delete("/{task_id}", response_model=TaskResponseSchema)
def delete_existing_task(task_id: int, db: Session = Depends(get_db)):
    deleted_task = delete_task(db, task_id)
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task