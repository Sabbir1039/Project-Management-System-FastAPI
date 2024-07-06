from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user, project, task, auth
from .database import engine, Base
from .models import user as user_model, project as project_model, task as task_model

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    # "http://your-frontend-domain.com", 
]

# CORSMiddleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from these origins
    allow_credentials=True,  # Allow cookies to be sent with requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(project.router, prefix="/projects", tags=["projects"])
app.include_router(task.router, prefix="/tasks", tags=["tasks"])
app.include_router(auth.router, tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Project Management API"}