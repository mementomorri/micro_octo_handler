from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase


# Асинхронный движок подключения к БД
engine = create_async_engine("sqlite+aiosqlite:///user.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


# Базовый класс из sqlalchemy для еаследования в таблицы
class Base(DeclarativeBase):
    pass


async def create_tables():
    """Асинхронная функция для создания таблиц"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    """Асинхронная функция для удаление таблиц, используется для тестирования"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Создание новой асинхронной сессии соединеия с БД"""
    async with new_session() as session:
        yield session
