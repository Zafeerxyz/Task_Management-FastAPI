from fastapi import FastAPI
from app.database import create_table
from app.routes.tasks import tasks_router

app = FastAPI()


@app.on_event("startup")
def startup():
    create_table()


app.include_router(tasks_router)


@app.get("/")
def welcome():
    return {"message": "Welcome to Task Management API"}