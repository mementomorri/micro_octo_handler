from datetime import date

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, Date, Integer
from db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Структура для храния сведений о пользователе в токене"""

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    paid_access: Mapped[bool] = mapped_column(Boolean)
    free_messages_left: Mapped[int] = mapped_column(Integer)
    refresh_at: Mapped[date] = mapped_column(Date)
