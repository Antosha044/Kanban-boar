from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from src.models.models import Project, projects_users, User
from src.schemas.project import ProjectCreate, ProjectUpdate
from uuid import UUID, uuid4
from datetime import datetime


async def create_project(session: AsyncSession, project_data: ProjectCreate) -> Project:
    new_project = Project(
        id=uuid4(),  
        name=project_data.name,
        description=project_data.description,
        create_time=datetime.utcnow(),
        last_update=datetime.utcnow()
    )
    session.add(new_project)  
    await session.commit()    
    await session.refresh(new_project)  
    return new_project


async def get_project_by_id(session: AsyncSession, project_id: str) -> Project | None:
    result = await session.execute(select(Project).where(Project.id == project_id))
    return result.scalar_one_or_none()


async def get_all_projects(session: AsyncSession) -> list[Project]:
    result = await session.execute(select(Project))
    return result.scalars().all()


async def update_project(session: AsyncSession, project_id: UUID, project_data: ProjectUpdate) -> Project | None:
    result = await session.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        return None

    for key, value in project_data.model_dump(exclude_unset=True).items():
        setattr(project, key, value)

    project.last_update = datetime.utcnow() 
    await session.commit()
    await session.refresh(project)
    return project


async def delete_project(session: AsyncSession, project_id: UUID) -> bool:
    result = await session.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        return False

    await session.delete(project)
    await session.commit()
    return True


async def add_user_to_project(session: AsyncSession, project_id: UUID, user_id: UUID) -> None:
    await session.execute(
        insert(projects_users).values(project_id=project_id, user_id=user_id)
    )
    await session.commit()


async def remove_user_from_project(session: AsyncSession, project_id: UUID, user_id: UUID) -> None:
    await session.execute(
        delete(projects_users).where(
            projects_users.c.project_id == project_id,
            projects_users.c.user_id == user_id
        )
    )
    await session.commit()


async def get_project_users(session: AsyncSession, project_id: UUID) -> list[User]:
    result = await session.execute(
        select(User)
        .join(projects_users)
        .where(projects_users.c.project_id == project_id)
    )
    return result.scalars().all()