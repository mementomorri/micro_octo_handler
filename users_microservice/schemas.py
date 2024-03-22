from pydantic import BaseModel, ConfigDict


class SUserAdd(BaseModel):
    """Структура для добавления пользователя"""

    paid_access: bool = False
    free_messages_left: int = 10
    refresh_at: int = 86400


class SUserData(SUserAdd):
    """Структура для храние информации о пользователе"""

    id: int

    model_config = ConfigDict(from_attributes=True)


class SUserId(BaseModel):
    """Шаблон ответа на добавление пользователя"""

    ok: bool
    user_id: int


class SOpStatus(BaseModel):
    """Шаблон ответа на выполнение простой операции"""

    ok: bool
