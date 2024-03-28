import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.user_microservice.conf import TEST_USER_DB
from src.user_microservice.microservice import app
from src.user_microservice.db import get_async_session, Base


engine_test = create_async_engine(f"sqlite+aiosqlite:///{TEST_USER_DB}")
new_session = async_sessionmaker(engine_test, expire_on_commit=False)


async def override_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Создание новой асинхронной сессии соединеия с БД"""
    async with new_session() as session:
        yield session


app.dependency_overrides[get_async_session] = override_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # TEARDOWN
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# SETUP
@pytest.fixture(scope="session")
def event_loop(request):
    """Создает инстанс стандартного цикла событий для каждого теста"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
