from typing import Optional
from datetime import date

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема для считывания данных о пользователе"""

    id: int
    paid_access: bool
    free_messages_left: int
    refresh_at: date
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 2,
                "email": "mementomorimore@gmail.com",
                "paid_access": False,
                "free_messages_left": 10,
                "refresh_at": "2024-03-24",
                "is_active": True,
                "is_superuser": False,
                "is_verified": False,
            }
        }


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания данных о пользователе"""

    email: str
    paid_access: bool
    free_messages_left: int
    refresh_at: date
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    class Config:
        schema_extra = {
            "example": {
                "email": "mementomorimore@gmail.com",
                "password": "thisisverysecretpassword",
                "paid_access": False,
                "free_messages_left": 10,
                "refresh_at": "2024-03-24",
                "is_active": True,
                "is_superuser": False,
                "is_verified": False,
            }
        }


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления данных о пользователе"""

    id: int
    paid_access: bool
    free_messages_left: int
    refresh_at: date

    class Config:
        schema_extra = {
            "example": {
                "id": 2,
                "paid_access": False,
                "free_messages_left": 10,
                "refresh_at": "2024-03-24",
            }
        }
