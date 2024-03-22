from pydantic import BaseModel, ConfigDict
from datetime import datetime


class SUserAdd(BaseModel):
    """Структура для добавления пользователя"""

    paid_access: bool = False
    free_messages_left: int = 10
    refresh_at: int = 86400
    # refresh_at: datetime = datetime.


class SUserData(SUserAdd):
    """Структура для храние информации о пользователе"""

    id: int

    model_config = ConfigDict(from_attributes=True)


class SMessageAdd(BaseModel):
    """Структура для получения сообщения на обработку"""

    user_id: int
    message: str


class SMessageResponse(BaseModel):
    ok: bool
    response: str
