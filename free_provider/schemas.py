from pydantic import BaseModel, ConfigDict


class SUserAdd(BaseModel):
    """Структура для добавления пользователя"""

    access: bool = True
    free_messages_left: int = 10
    refresh_in: int = 86400


class SUserData(SUserAdd):
    """Структура для храние информации о пользователе"""

    id: int

    model_config = ConfigDict(from_attributes=True)


class SUserId(BaseModel):
    """Шаблон ответа на добавление пользователя"""

    ok: bool = True
    user_id: int
