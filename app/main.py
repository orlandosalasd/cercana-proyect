from fastapi import FastAPI
from app.api.routes import auth, task

app = FastAPI()

app.include_router(auth.router)
app.include_router(task.router)
