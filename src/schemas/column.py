from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class ColumnBase(BaseModel):
    name: str
    description: Optional[str] = None


class ColumnCreate(ColumnBase):
    project_id: UUID


class ColumnUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ColumnOut(ColumnBase):
    id: UUID
    project_id: UUID
    tasks: list = []
    # или List[TaskOut] при импорте Task схем
    class Config:
        from_attributes = True
