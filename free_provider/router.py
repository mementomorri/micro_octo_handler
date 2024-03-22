from fastapi import APIRouter, Depends
import httpx

from schemas import SMessageAdd, SUserData, SMessageResponse

from typing import Annotated
import asyncio
import os

# Содаю отдельный роутер для для пространства /users
router = APIRouter(prefix="/free_provider", tags=["Бесплатный провайдер"])
# USERS_TEST_PORT = os.environ.get("USERS_TEST_PORT")
USERS_TEST_PORT = 8000
USERS_API_URL = "http://0.0.0.0:" + str(USERS_TEST_PORT) + "/users"


async def request_user_data(client, user_id):
    response = await client.get(USERS_API_URL + str(user_id))
    return response.text


async def task(user_id):
    async with httpx.AsyncClient() as client:
        tasks = request_user_data(client, user_id)
        result = await asyncio.gather(tasks)
        return result


@router.get("")
async def handle_message(data: Annotated[SMessageAdd, Depends()]) -> SMessageResponse:
    """Путь на добавление пользователя"""
    user_data = await task(data.user_id)
    decoded_user = SUserData.model_validate_json(user_data[0])
    if decoded_user.free_messages_left > 0:
        return {"ok": True, "response": data.message[::-1]}
    if decoded_user.paid_access:
        return {
            "ok": True,
            "response": "Redirecting to paid service",
        }
    return {
        "ok": False,
        "response": "Access denied",
    }
