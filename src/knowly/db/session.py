
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.knowly.core.config import settings


# Create the asynchronous database engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)


# Create a reusable session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# Dependency for providing database sessions
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
