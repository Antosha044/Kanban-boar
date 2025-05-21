from pydantic import BaseModel
from uuid import UUID
from typing import Optional, List

from src.schemas.task import TaskOut

class ColumnBase(BaseModel):
    name: str
    description: Optional[str] = None
    order: Optional[int] = None 


class ColumnCreate(ColumnBase):
    project_id: UUID


class ColumnUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None

class ColumnOut(ColumnBase):
    id: UUID
    project_id: UUID
    order: int 
    tasks: List[TaskOut] = []
    class Config:
        from_attributes = True
