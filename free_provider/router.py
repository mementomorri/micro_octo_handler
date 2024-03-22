from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
import httpx

from schemas import SMessageAdd, SUserData, SMessageResponse

from typing import Annotated, Callable
import asyncio
import os

# Содаю отдельный роутер для для пространства /users
router = APIRouter(prefix="/free_provider", tags=["Бесплатный провайдер"])
# USERS_TEST_PORT = os.environ.get("USERS_TEST_PORT")
USERS_TEST_PORT = "8000"
PAID_PROVIDER_PORT = "2198"
BASE_URL = "http://0.0.0.0:"
USERS_API_URL = BASE_URL + USERS_TEST_PORT + "/users"


async def request_user_data(client: httpx.AsyncClient, user_id: int) -> str:
    response = await client.get(USERS_API_URL + str(user_id))
    return response.text


async def patch_messages_left(
    client: httpx.AsyncClient, user_id: int, messages_left: int
) -> str:
    response = await client.patch(
        USERS_API_URL + str(user_id) + "/messages?messages_left=" + str(messages_left),
    )
    return response.text


async def task(func: Callable, **kwargs):
    async with httpx.AsyncClient() as client:
        tasks = func(client, **kwargs)
        result = await asyncio.gather(tasks)
        return result


@router.get("")
async def handle_message(
    data: Annotated[SMessageAdd, Depends()],
) -> SMessageResponse:
    """Путь на добавление пользователя"""
    user_data = await task(request_user_data, user_id=data.user_id)
    decoded_user = SUserData.model_validate_json(user_data[0])
    if decoded_user.free_messages_left > 0:
        await task(
            patch_messages_left,
            user_id=decoded_user.id,
            messages_left=decoded_user.free_messages_left - 1,
        )
        return SMessageResponse.model_validate(
            {"ok": True, "response": data.message[::-1]}
        )
    if decoded_user.paid_access:
        return RedirectResponse(
            BASE_URL + PAID_PROVIDER_PORT
            # + "/paid_provider?user_id="
            # + str(data.user_id)
            # + "&message="
            # + str(data.message),
        )
    return SMessageResponse.model_validate(
        {
            "ok": False,
            "response": "Access denied",
        }
    )
