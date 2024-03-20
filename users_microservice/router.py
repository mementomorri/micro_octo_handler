from fastapi import APIRouter, Depends

from repo import UserRepository
from schemas import SUserAdd, SUserData, SUserId

from typing import Annotated


# Содаю отдельный роутер для для пространства /users
router = APIRouter(prefix="/users", tags=["Микросервис работы с пользователями"])


@router.post("")
async def add_user(user: Annotated[SUserAdd, Depends()]) -> SUserId:
    """Путь на добавление пользователя"""
    user_id = await UserRepository.user_add(user)
    return {"status": 200, "user_id": user_id}


@router.get("")
async def get_users() -> list[SUserData]:
    """Путь на получение всех пользователей"""
    users = await UserRepository.get_all()
    return users


@router.get("{user_id}")
async def get_user(user_id: int) -> SUserData:
    """Вернет данные о конкретном ползователе из БД"""
    user = await UserRepository.get_user(user_id)
    return user
