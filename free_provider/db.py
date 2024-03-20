from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Асинхронный движок подключения к БД
engine = create_async_engine("sqlite+aiosqlite:///users.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


# Базовый класс из sqlalchemy для еаследования в таблицы
class Base(DeclarativeBase):
    pass


class UsersOrm(Base):
    """Таблица пользователей"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    access: Mapped[bool]
    free_messages_left: Mapped[int]
    refresh_in: Mapped[int]


async def create_tables():
    """Асинхронная функция для создания таблиц"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    """Асинхронная функция для удаление таблиц, используется для тестирования"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
