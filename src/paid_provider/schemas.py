from datetime import date

from pydantic import BaseModel


class SUserRead(BaseModel):
    """Структура для считывания данных пользователя из токена"""

    sub: str
    exp: int
    email: str
    paid_access: bool
    free_messages_left: int
    refresh_at: str


class SUserData(BaseModel):
    """Структура для представления данных о пользователе"""

    id: str
    paid_access: bool
    free_messages_left: int
    refresh_at: str
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


class SMessageAdd(BaseModel):
    """Структура для получения сообщения на обработку"""

    token: str
    message: str


class SMessageResponse(BaseModel):
    """Структура для ответа на сообщение"""

    ok: bool
    response: str
