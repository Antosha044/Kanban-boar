from uuid import uuid4, UUID
from datetime import datetime

from sqlalchemy.orm import selectinload

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import Task, TaskLog, tasks_users, User
from src.schemas.task import TaskCreate, TaskUpdate

from typing import Optional
from sqlalchemy import func, asc, desc

async def create_task(session: AsyncSession, task_data: TaskCreate) -> Task:
    new_task = Task(
        id=uuid4(),
        name=task_data.name,
        description=task_data.description,
        column_id=task_data.column_id,
        create_time=datetime.utcnow(),
        last_update=datetime.utcnow()
    )
    session.add(new_task)
    await session.flush() 

    log = TaskLog(
        id=uuid4(),
        task_id=new_task.id,
        create_time=datetime.utcnow(),
        message=f"Task '{new_task.name}' was created."
    )
    session.add(log)

    await session.commit()
    result = await session.execute(
        select(Task)
        .where(Task.id == new_task.id)
        .options(
            selectinload(Task.users),
            selectinload(Task.logs),
            selectinload(Task.column)
        )
    )
    return result.scalar_one()

async def get_task_by_id(session: AsyncSession, task_id: UUID) -> Task | None:
    result = await session.execute(
        select(Task)
        .where(Task.id == task_id)
        .options(
            selectinload(Task.users), 
            selectinload(Task.logs),   
            selectinload(Task.column)  
        )
    )
    return result.scalar_one_or_none()

async def get_tasks_by_column(
    session: AsyncSession,
    column_id: UUID,
    name_contains: Optional[str] = None,
    user_id: Optional[UUID] = None,
    sort_by_create_time: Optional[str] = None,  
    sort_by_update_time: Optional[str] = None  
) -> list[Task]:
    query = (
        select(Task)
        .where(Task.column_id == column_id)
        .options(
            selectinload(Task.users),
            selectinload(Task.logs),
            selectinload(Task.column)
        )
    )

    if name_contains:
        query = query.where(func.lower(Task.name).contains(name_contains.lower()))

    if user_id:
        query = query.join(tasks_users).where(tasks_users.c.user_id == user_id)

    if sort_by_create_time:
        if sort_by_create_time.lower() == 'desc':
            query = query.order_by(desc(Task.create_time))
        else:
            query = query.order_by(asc(Task.create_time))
    
    if sort_by_update_time:
        if sort_by_update_time.lower() == 'desc':
            query = query.order_by(desc(Task.last_update))
        else:
            query = query.order_by(asc(Task.last_update))

    result = await session.execute(query)
    return result.scalars().all()


async def update_task(session: AsyncSession, task_id: UUID, task_data: TaskUpdate) -> Task | None:
    task = await get_task_by_id(session, task_id)
    if not task:
        return None

    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    task.last_update = datetime.utcnow()

    log = TaskLog(
        id=uuid4(),
        task_id=task.id,
        create_time=datetime.utcnow(),
        message=f"Task '{task.name}' was updated."
    )
    session.add(log)

    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(session: AsyncSession, task_id: UUID) -> bool:
    task = await get_task_by_id(session, task_id)
    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True


async def add_user_to_task(session: AsyncSession, task_id: UUID, user_id: UUID) -> None:
    await session.execute(
        tasks_users.insert().values(task_id=task_id, user_id=user_id)
    )
    await session.commit()


async def remove_user_from_task(session: AsyncSession, task_id: UUID, user_id: UUID) -> None:
    await session.execute(
        tasks_users.delete().where(
            and_(
                tasks_users.c.task_id == task_id,
                tasks_users.c.user_id == user_id
            )
        )
    )
    await session.commit()


async def get_task_logs(session: AsyncSession, task_id: UUID) -> list[TaskLog]:
    result = await session.execute(
        select(TaskLog).where(TaskLog.task_id == task_id)
    )
    return result.scalars().all()




async def get_users_by_task(session: AsyncSession, task_id: UUID) -> list[User]:
    result = await session.execute(
        select(User)
        .join(tasks_users)
        .where(tasks_users.c.task_id == task_id)
    )
    return result.scalars().all()