from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from journal.schema import *
from config.settings import Settings

DATABASE_URL = Settings().psql_conn_string

engine = create_async_engine(DATABASE_URL, echo=Settings().debug, future=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db() -> AsyncSession:
    # async_session = sessionmaker(
    #     engine, class_ = AsyncSession, expire_on_commit=False
    # )

    async with AsyncSession(engine) as session:
        yield session
        await session.close()
