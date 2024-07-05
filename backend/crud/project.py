from sqlalchemy.orm import Session
from ..schemas.project import ProjectCreateSchema
from ..models.project import Project

def create_project(db: Session, project: ProjectCreateSchema, owner_id: int):
    new_project = Project(**project.dict(), owner_id=owner_id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

def get_projects(db: Session, owner_id: int, skip: int = 0, limit: int = 10):
    return db.query(Project).filter(Project.owner_id == owner_id).offset(skip).limit(limit).all()

def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    if db_project:
        db.delete(db_project)
        db.commit()
        return db_project
    return None