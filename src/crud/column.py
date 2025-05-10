from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.models import BoardColumn, Task
from src.schemas.column import ColumnCreate, ColumnUpdate
from sqlalchemy.orm import selectinload

async def create_column(session: AsyncSession, column_data: ColumnCreate) -> BoardColumn:
    new_column = BoardColumn(
        id=uuid4(),
        name=column_data.name,
        description=column_data.description,
        project_id=column_data.project_id
    )
    session.add(new_column)
    await session.commit()
    await session.refresh(new_column)
    return new_column


async def get_column_by_id(session: AsyncSession, column_id: UUID) -> BoardColumn | None:
    result = await session.execute(
        select(BoardColumn)
        .where(BoardColumn.id == column_id)
        .options(
            selectinload(BoardColumn.tasks).selectinload(Task.users),
            selectinload(BoardColumn.tasks).selectinload(Task.logs)
        )
    )
    return result.scalar_one_or_none()

async def get_columns_by_project(session: AsyncSession, project_id: UUID) -> list[BoardColumn]:
    result = await session.execute(
        select(BoardColumn)
        .where(BoardColumn.project_id == project_id)
        .options(
            selectinload(BoardColumn.tasks).selectinload(Task.users),
            selectinload(BoardColumn.tasks).selectinload(Task.logs)
        )
    )
    return result.scalars().all()

async def update_column(session: AsyncSession, column_id: UUID, column_data: ColumnUpdate) -> BoardColumn | None:
    result = await session.execute(
        select(BoardColumn)
        .where(BoardColumn.id == column_id)
        .options(
            selectinload(BoardColumn.tasks).selectinload(Task.users),
            selectinload(BoardColumn.tasks).selectinload(Task.logs)
        )
    )
    column = result.scalar_one_or_none()
    if not column:
        return None
    for key, value in column_data.model_dump(exclude_unset=True).items():
        setattr(column, key, value)
    await session.commit()
    await session.refresh(column)
    return column

async def delete_column(session: AsyncSession, column_id: UUID) -> bool:
    result = await session.execute(select(BoardColumn).where(BoardColumn.id == column_id))
    column = result.scalar_one_or_none()
    if not column:
        return False

    await session.delete(column)
    await session.commit()
    return True
