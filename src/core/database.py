# Здесь будут располагаться система подключения и инициализации базы данных
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.settings import settings

engine = create_async_engine(
    url = settings.DATABASE_URL_asyncpg,
    echo = True
    #pool_size = 5
    #max_overflow = 10
)
#фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

Base = declarative_base()
