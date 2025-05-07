from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    column_id: UUID


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    column_id: Optional[UUID] = None


class TaskOut(TaskBase):
    id: UUID
    column_id: UUID
    create_time: datetime
    last_update: datetime
    users: list = []
    logs: list = []

    class Config:
        from_attributes = True
