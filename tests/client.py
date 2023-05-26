import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.testclient import TestClient

from database.psql import get_db
from app.main import app


class GetDBOverride:
    def __init__(self, engine):
        self.engine = engine

    async def __call__(self) -> AsyncSession:
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        async with AsyncSession(self.engine) as session:
            yield session
            await session.close()


@pytest.fixture(scope='session')
def test_client():
    engine = create_async_engine('sqlite+aiosqlite:///:memory:')

    app.dependency_overrides[get_db] = GetDBOverride(engine)

    test_client = TestClient(app)
    yield test_client
    test_client.close()
