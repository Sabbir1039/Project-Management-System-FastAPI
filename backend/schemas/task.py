from pydantic import BaseModel, Field
from typing import Optional

class TaskBaseSchema(BaseModel):
    title: str
    description: str

class TaskCreateSchema(TaskBaseSchema):
    project_id: int

class TaskResponseSchema(TaskBaseSchema):
    id: int
    project_id: int

    class Config:
        from_attributes = True

class TaskUpdateSchema(TaskBaseSchema):
    title: Optional[str] = Field(None, title="Title of the task")
    description: Optional[str] = Field(None, title="Description of the task")
    project_id: Optional[int] = Field(None, title="ID of the associated project")

    class Config:
        from_attributes = True