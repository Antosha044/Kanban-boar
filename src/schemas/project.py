from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    last_update: Optional[datetime] = None


class ProjectOut(ProjectBase):
    id: UUID
    create_time: datetime
    last_update: datetime

    class Config:
        from_attributes = True

