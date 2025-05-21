# Здесь модели таблиц из SQLAlchemy
#from __future__ import annotations
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Table, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import uuid
from src.core.database import Base



class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True,nullable=False)
    full_name: Mapped[str] = mapped_column(String(255))
    reg_time: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    email: Mapped[str] = mapped_column(String(255),unique=True,nullable=False)
    password: Mapped[str] = mapped_column(String(255),nullable=False)

    projects: Mapped[list["Project"]] = relationship("Project",secondary="projects_users",back_populates="users")
    tasks: Mapped[list["Task"]] = relationship("Task",secondary="tasks_users",back_populates="users")

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255),nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    create_time: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_update: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    users: Mapped[list["User"]] = relationship("User",secondary="projects_users",back_populates="projects")
    columns: Mapped[list["BoardColumn"]] = relationship("BoardColumn",back_populates="project",cascade="all, delete-orphan")

projects_users = Table(
    "projects_users",
    Base.metadata,
    Column("project_id", UUID(as_uuid=True), ForeignKey("projects.id")),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"))
)

class BoardColumn(Base):
    __tablename__ = "columns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), nullable=False)
    description: Mapped[str] = mapped_column(String(255),nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    project: Mapped["Project"] = relationship("Project", back_populates="columns")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="column", cascade="all, delete-orphan", lazy="selectin")

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    column_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("columns.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    create_time: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_update: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    column: Mapped["BoardColumn"] = relationship("BoardColumn", back_populates="tasks")
    users: Mapped[list["User"]] = relationship("User",secondary="tasks_users",back_populates="tasks")
    logs: Mapped[list["TaskLog"]] = relationship("TaskLog",back_populates="task",cascade="all, delete-orphan")

tasks_users = Table(
    "tasks_users",
    Base.metadata,
    Column("task_id", UUID(as_uuid=True), ForeignKey("tasks.id")),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"))
)

class TaskLog(Base):
    __tablename__ = "task_log"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    create_time: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    task: Mapped["Task"] = relationship("Task", back_populates="logs")
