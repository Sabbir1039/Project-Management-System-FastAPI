from fastapi import FastAPI
from .routers import user, project, task, auth
from .database import engine, Base
from .models import user as user_model, project as project_model, task as task_model

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(project.router, prefix="/projects", tags=["projects"])
app.include_router(task.router, prefix="/tasks", tags=["tasks"])
app.include_router(auth.router, tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Project Management API"}