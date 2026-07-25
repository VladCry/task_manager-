from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, users, tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API", version="1.0.0")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Task Management API. Docs at /docs"}
