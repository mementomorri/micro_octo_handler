from fastapi import APIRouter, Depends
import httpx

from schemas import SMessageAdd, SUserData, SMessageResponse

from typing import Annotated
import asyncio

# Содаю отдельный роутер для для пространства /users
router = APIRouter(prefix="/free_provider", tags=["Бесплатный провайдер"])

USERS_API_URL = "http://0.0.0.0:8000/users"


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
        return {"status": "acepted", "response": data.message[::-1]}
    return {
        "status": "access denied",
        "response": "redirecting to paid service",
    }
