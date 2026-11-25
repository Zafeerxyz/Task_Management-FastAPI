from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str | None = None
    status: Literal["pending", "in_progress", "completed"] = "pending"
    priority: Literal["low", "medium", "high"] = "medium"
    due_date: datetime  | None = None
    
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    due_date: datetime | None = None
    
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: str
    priority: str
    due_date: datetime  | None
    
class TaskPatch(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = None
    status: Literal["pending", "in_progress", "completed"] | None = None
    priority: Literal["low", "medium", "high"] | None = None
    due_date: datetime | None = None