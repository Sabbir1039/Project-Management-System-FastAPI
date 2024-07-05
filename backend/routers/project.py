from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas.project import ProjectCreateSchema, ProjectResponseSchema, ProjectUpdateSchema
from ..database import get_db
from ..crud.project import create_project, get_project, get_projects, delete_project
from ..dependencies import get_current_user_id

router = APIRouter()

@router.post("/", response_model=ProjectResponseSchema)
def create_new_project(
    project: ProjectCreateSchema,
    db: Session = Depends(get_db),
    owner_id: int = Depends(get_current_user_id)):
    return create_project(db=db, project=project, owner_id=owner_id)

@router.get("/{project_id}", response_model=ProjectResponseSchema)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = get_project(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.put("/update/{project_id}", response_model=ProjectResponseSchema)
def update_project(project_id: int, project: ProjectUpdateSchema, db: Session = Depends(get_db)):
    try:
        db_project = get_project(db, project_id)
        if db_project:
            if project.name:
                db_project.name = project.name
            if project.description:
                db_project.description = project.description
            db.commit()
            db.refresh(db_project)
            return db_project
        else:
            raise HTTPException(status_code=404, detail="Project not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/", response_model=List[ProjectResponseSchema])
def read_projects(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    owner_id: int = Depends(get_current_user_id)):
    projects = get_projects(db, owner_id=owner_id, skip=skip, limit=limit)
    return projects

@router.delete("/delete/{project_id}", response_model=ProjectResponseSchema)
def remove_project(project_id: int, db: Session = Depends(get_db)):
    db_project = delete_project(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project
