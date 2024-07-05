from pydantic import BaseModel, EmailStr
from typing import List, Optional
from ..schemas.task import TaskResponseSchema

# Project Schemas
class ProjectBaseSchema(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreateSchema(ProjectBaseSchema):
    pass

class UpdateProjectSchema(ProjectBaseSchema):
    name: Optional[str]
    description: Optional[str]

class ProjectResponseSchema(ProjectBaseSchema):
    id: int
    owner_id: int
    tasks: List[TaskResponseSchema] = []

    class Config:
        from_attributes = True