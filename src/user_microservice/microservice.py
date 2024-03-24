from db import create_tables, drop_tables

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate, UserUpdate
from auth.models import User

from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends


# Жизненный цикл приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Тестовый вариант, при котором таблица пользователей
    каждый раз пересоздается
    """
    await drop_tables()
    print("БД токенов подчищена")
    await create_tables()
    print("и готова к работе!")
    yield
    print("Работа микросервиса польозвателей завершена")


app = FastAPI(title="Микросервис аутентификации пользователей", lifespan=lifespan)
current_user = fastapi_users.current_user()

# Подключение роутера аутентификации пользователей
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Аутентификация"],
)

# Подключение роутера регистрации пользователей
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Аутентификация"],
)

# Подключение роутера верификации пользователей
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["Аутентификация"],
)

# Подключение роутера считывания данных о пользователе
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Пользователи"],
)


@app.get("/welcome", tags=["Тестовые точки"])
def protected_route(user: User = Depends(current_user)) -> dict:
    """Тестовая точка входа для проверки аутентификации"""
    return {"ok": True, "response": f"Welcome, {user.email}"}
