from fastapi import APIRouter, Depends

from repo import UserRepository
from schemas import SUserAdd, SUserData, SUserId, SOpStatus

from typing import Annotated


# Содаю отдельный роутер для для пространства /users
router = APIRouter(prefix="/users", tags=["Микросервис работы с пользователями"])


@router.post("")
async def add_user(user: Annotated[SUserAdd, Depends()]) -> SUserId:
    """Путь на добавление пользователя"""
    user_id = await UserRepository.user_add(user)
    return {"ok": True, "user_id": user_id}


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


@router.patch("{user_id}/free_messages")
async def patch_free_messages(user_id: int, messages_left: int) -> SOpStatus:
    result = await UserRepository.patch_free_messages(user_id, messages_left)
    return {"ok": True} if result else {"ok": False}
