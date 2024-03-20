from fastapi import APIRouter, Depends

from repo import UserRepository
from schemas import SUserAdd, SUserData, SUserId

from typing import Annotated


# Содаю отдельный роутер для для пространства /users
router = APIRouter(prefix="/users", tags=["Бесплатный провайдер"])


@router.post("")
async def add_user(user: Annotated[SUserAdd, Depends()]) -> SUserId:
    """Путь на добавление пользователя"""
    user_id = await UserRepository.user_add(user)
    return {"ok": True, "user_id": user_id}


@router.get("")
async def get_users() -> list[SUserData]:
    """Путь на получение всех пользователей"""
    user = await UserRepository.get_all()
    return user
