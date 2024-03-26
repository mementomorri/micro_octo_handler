from fastapi import APIRouter, Depends, HTTPException

from schemas import SMessageAdd, SMessageResponse
from utils import verify_user, get_user_data
from conf import USERS_TEST_PORT, FREE_PROVIDER_PORT, BASE_URL

from typing import Annotated

# Содаю отдельный роутер для для пространства /users
router = APIRouter(prefix="/paid_provider", tags=["Обработка сообщений"])

USERS_API_URL = str(BASE_URL) + str(USERS_TEST_PORT) + "/user"
FREE_PROVIDER_API_URL = (
    str(BASE_URL) + str(FREE_PROVIDER_PORT) + "/free_provider/redirected"
)


@router.post("")
async def handle_message(data: Annotated[SMessageAdd, Depends()]) -> SMessageResponse:
    """Конечная точка для оплаченой обработки сообщений"""
    await verify_user(data.token)
    user_data = await get_user_data(data.token)
    current_messages_left = user_data["free_messages_left"]
    if current_messages_left > 0:
        return SMessageResponse.model_validate(
            {
                "ok": True,
                "response": f"Запрос перенаправлен на платный провайдер. {FREE_PROVIDER_API_URL}",
            }
        )

    elif user_data["paid_access"]:
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


@router.get("/redirected")
async def redirect_response() -> dict:
    """Конечная точка для обработки перенаправления"""
    return {
        "ok": True,
        "response": "Ваш запрос был перенаправлен на платный провайдер.",
    }
