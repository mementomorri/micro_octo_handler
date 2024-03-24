from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from schemas import SMessageAdd, SMessageResponse
from utils import verify_current_user, renew_user_data

from typing import Annotated

# Содаю отдельный роутер для для пространства /users
router = APIRouter(prefix="/paid_provider", tags=["Обработка сообщений"])

USERS_TEST_PORT = "8000"
FREE_PROVIDER_PORT = "2197"
BASE_URL = "http://0.0.0.0:"
USERS_API_URL = BASE_URL + USERS_TEST_PORT + "/user"


@router.post("")
async def handle_message(data: Annotated[SMessageAdd, Depends()]) -> SMessageResponse:
    """Конечная точка для оплаченой обработки сообщений"""
    await verify_current_user(data.token)
    current_user_data = await renew_user_data(data.token)
    current_messages_left = current_user_data["free_messages_left"]
    if current_messages_left > 0:
        return RedirectResponse(BASE_URL + FREE_PROVIDER_PORT + "/free_provider", 303)
    elif current_user_data["paid_access"]:
        return SMessageResponse.model_validate(
            {"ok": True, "response": data.message[::-1]}  # Имитация обработки сообщения
        )
    else:
        raise HTTPException(
            403,
            {
                "ok": False,
                "response": "Бесплатных сообщений не осталось. Доступ к платному провайдеру отсутствует",
            },
        )
