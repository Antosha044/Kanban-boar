from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List
from datetime import datetime


from src.schemas.task_log import TaskLogOut
from src.schemas.user import UserOut

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
    users: List[UserOut] = []  
    logs: List[TaskLogOut] = []  
    class Config:
        from_attributes = True
