from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from utils import renew_user_data, get_current_user, update_current_user
from schemas import SMessageAdd, SMessageResponse

from typing import Annotated


# Содаю отдельный роутер для для пространства /free_provider
router = APIRouter(prefix="/free_provider", tags=["Обработка сообщений"])

# В тестовом варианте храню переменные среды прямо в константах
USERS_TEST_PORT = "8000"
PAID_PROVIDER_PORT = "2198"
BASE_URL = "http://0.0.0.0:"
USERS_API_URL = BASE_URL + USERS_TEST_PORT + "/user"


@router.post("")
async def handle_message(data: Annotated[SMessageAdd, Depends()]) -> SMessageResponse:
    """Конечная точка для бесплатной обработки сообщений"""
    user_data = await get_current_user(data.token)
    current_user_data = await renew_user_data(data.token)
    current_messages_left = current_user_data["free_messages_left"]
    if current_messages_left > 0:
        await update_current_user(
            user_data.sub,
            user_data.email,
            current_messages_left - 1,
            current_user_data["paid_access"],
            current_user_data["refresh_at"],
            data.token,
        )
        return SMessageResponse.model_validate(
            {"ok": True, "response": data.message[::-1]}  # Имитация обработки сообщения
        )
    elif current_user_data["paid_access"]:
        return RedirectResponse(BASE_URL + PAID_PROVIDER_PORT + "/paid_provider", 303)
    else:
        raise HTTPException(
            403,
            {
                "ok": False,
                "response": "Бесплатных сообщений не осталось. Доступ к платному провайдеру отсутствует",
            },
        )
