from importlib.metadata import metadata

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from models.models import metadata

from utils.db_config import DATABASE_URL


async def create_tables():
    engine = create_async_engine(DATABASE_URL)
    metadata.bind = engine

    async with engine.begin() as connection:
        await connection.run_sync(metadata.create_all, bind=engine)


async_sessionmaker = sessionmaker(
    bind=create_async_engine(DATABASE_URL, echo=True),
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_async_session():
    async with async_sessionmaker() as session:
        try:
            yield session
        finally:
            await session.close()
