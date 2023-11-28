from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from contextlib import asynccontextmanager

from app.data.config import Settings

engine = create_async_engine(
    Settings.CONNECTION_STRING,
    echo=True
)


def async_session_generator():
    """getting async sqlalchemy session"""
    return sessionmaker(
        engine, class_=AsyncSession
    )


@asynccontextmanager
async def get_session() -> AsyncSession:
    """method for getting session without data leaks"""
    try:
        async_session = async_session_generator()

        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()