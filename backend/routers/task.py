from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..crud.task import create_task, get_project_tasks, get_task_by_id, update_task, delete_task
from ..schemas.task import TaskCreateSchema, TaskResponseSchema, TaskUpdateSchema
from ..database import get_db
from ..dependencies import get_current_user
from ..models.user import User
from typing import List

router = APIRouter()

@router.post("/", response_model=TaskResponseSchema)
def create_new_task(
    task: TaskCreateSchema,
    db: Session = Depends(get_db),
    curr_user: User = Depends(get_current_user)):
    
    if not curr_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    return create_task(db=db, task=task)

# Get all tasks for a specific project
@router.get("/project/{project_id}", response_model=List[TaskResponseSchema])
def read_project_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    curr_user: User = Depends(get_current_user)):
    
    if not curr_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    try:
        tasks = get_project_tasks(db, project_id)
        if tasks:
            return tasks
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not fetch task for the project!")
            
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# Get a specific task by its ID
@router.get("/{task_id}", response_model=TaskResponseSchema)
def read_task(task_id: int,
              db: Session = Depends(get_db),
              curr_user: User = Depends(get_current_user)):
    
    if not curr_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    try:
        task = get_task_by_id(db, task_id)
        if task:
            return task
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Update a task
@router.put("/update/{task_id}", response_model=TaskResponseSchema)
def update_existing_task(
    task_id: int,
    task_update: TaskUpdateSchema,
    db: Session = Depends(get_db),
    curr_user: User = Depends(get_current_user)):
    
    if not curr_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    try:
        updated_task = update_task(db, task_id, task_update)
        
        if updated_task:
            return updated_task
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    except Exception as e:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Delete a task
@router.delete("/delete/{task_id}", response_model=TaskResponseSchema)
def delete_existing_task(
    task_id: int,
    db: Session = Depends(get_db),
    curr_user: User = Depends(get_current_user)):
    
    if not curr_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    
    try:
        deleted_task = delete_task(db, task_id)
        
        if deleted_task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
        return deleted_task
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))