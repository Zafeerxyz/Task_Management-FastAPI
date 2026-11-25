from fastapi import APIRouter,HTTPException
from app.schemas.task import TaskCreate, TaskResponse, TaskPatch
from app.services.task_service import (create_task as create_task_service,
                                       get_all_tasks_selected,
                                       get_all_tasks,
                                       get_task_by_id,
                                       update_task,
                                       delete_task,
                                       patch_task)
from typing import Literal
from fastapi import Query


tasks_router = APIRouter()


@tasks_router.post("/tasks",response_model=TaskResponse,status_code=201)
def create_task(task: TaskCreate):
    return create_task_service(task)

@tasks_router.get("/all_tasks",response_model = list[TaskResponse],status_code = 201)
def get_tasks():
    return get_all_tasks()


@tasks_router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(status: Literal["pending", "in_progress", "completed"] | None = Query(default=None),
              priority: Literal["low", "medium", "high"] | None = Query(default=None)
            ):
    return get_all_tasks_selected(status, priority)


@tasks_router.get("/tasks/{task_id}",response_model = TaskResponse)
def get_task(task_id:int):
    task = get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code = 404,
                            detail = "Task not found")
    return task


@tasks_router.put("/tasks/{task_id}",response_model = TaskResponse)
def update_existing_task(task_id:int,task_update:TaskCreate):
    
    updated_task = update_task(task_id,task_update)
    
    if updated_task is None:
        raise HTTPException(status_code = 404,
                            detail = "Task not found")
    return updated_task


@tasks_router.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def patch_existing_task(task_id: int, task_update: TaskPatch):

    updated_task = patch_task(task_id, task_update)

    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return updated_task

@tasks_router.delete("/tasks/{task_id}")
def delete_task_selected(task_id:int):
    
    deleted_task = delete_task(task_id)
    
    if task_id is None:
        raise HTTPException(status_code = 404,
                            detail = "Task not found")
    
    return {
        "message":"Task deleted successfully",
        "task": deleted_task
    }
    