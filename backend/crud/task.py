from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from ..models.task import Task
from ..schemas.task import TaskCreateSchema, TaskResponseSchema, TaskUpdateSchema

def create_task(db: Session, task: TaskCreateSchema):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_project_tasks(db: Session, project_id: int):
    try:
        tasks = db.query(Task).filter(Task.project_id == project_id)
        return tasks
    except NoResultFound:
        return None


# Get a specific task by its ID
def get_task_by_id(db: Session, task_id: int):
    try:
        task = db.query(Task).filter(Task.id == task_id).one()
        return task
    except NoResultFound:
        return None

# Update a task
def update_task(db: Session, task_id: int, task_update: TaskUpdateSchema):
    task = get_task_by_id(db, task_id)
    if task is None:
        return None
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

# Delete a task
def delete_task(db: Session, task_id: int):
    task = get_task_by_id(db, task_id)
    if task is None:
        return None
    db.delete(task)
    db.commit()
    return task