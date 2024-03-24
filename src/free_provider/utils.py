from datetime import datetime
from fastapi import HTTPException
import httpx
import jwt
from typing import Callable
import asyncio
from pydantic import ValidationError
from schemas import SUserRead

# В тестовом варианте храню переменные среды прямо в константах
USERS_TEST_PORT = "8000"
PAID_PROVIDER_PORT = "2198"
BASE_URL = "http://0.0.0.0:"
USERS_API_URL = BASE_URL + USERS_TEST_PORT
AUTH_SECRET = "SECRET"
ALGORITHM = "HS256"


async def patch_user(
    client: httpx.AsyncClient,
    user_id: str,
    email: str,
    free_messages_left: int,
    paid_access: bool,
    refresh_at: str,
    token: str,
) -> int:
    """Обновление состояния пользователя в микросервисе аутентификаторе"""
    cookies = httpx.Cookies()
    cookies.set("octo_handler_user", token)
    response = await client.patch(
        USERS_API_URL + "/users/me",
        json={
            "email": email,
            "id": user_id,
            "paid_access": paid_access,
            "free_messages_left": free_messages_left,
            "refresh_at": refresh_at,
        },
        cookies=cookies,
    )

    return response.status_code


async def get_recent_user_data(client: httpx.AsyncClient, token: str) -> dict:
    """Получение последних изменених с микросервиса аутентификатра"""
    cookies = httpx.Cookies()
    cookies.set("octo_handler_user", token)
    response = await client.get(USERS_API_URL + "/users/me", cookies=cookies)
    return response.json()


async def verify_token(client: httpx.AsyncClient, email: str) -> int:
    """Верификация токена"""
    response = await client.post(
        USERS_API_URL + "/auth/request-verify-token",
        json={"email": email},
    )
    return response.status_code


async def task(func: Callable, **kwargs):
    """Запуск асинхронных запросов с httpx"""
    async with httpx.AsyncClient() as client:
        tasks = func(client, **kwargs)
        result = await asyncio.gather(tasks)
        return result


async def update_current_user(
    user_id: str,
    email: str,
    free_messages_left: int,
    paid_access: bool,
    refresh_at: str,
    token: str,
) -> bool:
    """Обработка изменений о пользователе"""
    resp = await task(
        patch_user,
        user_id=user_id,
        email=email,
        free_messages_left=free_messages_left,
        paid_access=paid_access,
        refresh_at=refresh_at,
        token=token,
    )
    if resp[0] != 200:
        raise HTTPException(404, {"details": "Пользователь не найден"})
    return True


async def renew_user_data(token: str) -> dict:
    """Обработка свежих данных о пользователе"""
    resp = await task(get_recent_user_data, token=token)
    resp = resp[0]
    return resp


async def get_current_user(token: str) -> SUserRead:
    """Декодирует токен и верифицирует его"""
    try:
        paylaod = jwt.decode(
            token, AUTH_SECRET, algorithms=[ALGORITHM], audience="fastapi-users:auth"
        )
        user_data = SUserRead(**paylaod)
        if datetime.fromtimestamp(user_data.exp) < datetime.utcnow():
            raise HTTPException(
                401, {"details": "Токен просрочен"}, {"WWW-Authenticate": "Bearer"}
            )

    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            403,
            {"details": "Невозможно провалидировать данные в токене"},
            {"WWW-Authenticate": "Bearer"},
        )

    verification = await task(verify_token, email=user_data.email)
    if verification[0] != 202:
        raise HTTPException(404, {"details": "Пользователь не найден"})

    return user_data
