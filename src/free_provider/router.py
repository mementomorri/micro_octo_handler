from fastapi import APIRouter, Depends, HTTPException

from utils import get_user_data, verify_user, update_current_user
from schemas import SMessageAdd, SMessageResponse

from typing import Annotated
from conf import USERS_TEST_PORT, PAID_PROVIDER_PORT, BASE_URL


# Содаю отдельный роутер для для пространства /free_provider
router = APIRouter(prefix="/free_provider", tags=["Обработка сообщений"])

USERS_API_URL = str(BASE_URL) + str(USERS_TEST_PORT) + "/user"
PAID_PROVIDER_API_URL = (
    str(BASE_URL) + str(PAID_PROVIDER_PORT) + "/paid_provider/redirected"
)


@router.post("")
async def handle_message(data: Annotated[SMessageAdd, Depends()]) -> SMessageResponse:
    """Конечная точка для бесплатной обработки сообщений"""
    await verify_user(data.token)
    user_data = await get_user_data(data.token)
    current_messages_left = user_data["free_messages_left"]
    if current_messages_left > 0:
        await update_current_user(
            user_data["id"],
            user_data["email"],
            current_messages_left - 1,
            user_data["paid_access"],
            user_data["refresh_at"],
            data.token,
        )
        return SMessageResponse.model_validate(
            {"ok": True, "response": data.message[::-1]}  # Имитация обработки сообщения
        )
    elif user_data["paid_access"]:
        return SMessageResponse.model_validate(
            {
                "ok": True,
                "response": f"Запрос перенаправлен на платный провайдер. {PAID_PROVIDER_API_URL}",
            }
        )
    else:
        raise HTTPException(
            403,
            {
                "ok": False,
                "response": "Бесплатных сообщений не осталось. Доступ к платному провайдеру отсутствует",
            },
        )


@router.get("/redirected")
async def redirect_response() -> dict:
    """Конечная точка для обработки перенаправления"""
    return {
        "ok": True,
        "response": "Ваш запрос был перенаправлен на бесплатный провайдер.",
    }
