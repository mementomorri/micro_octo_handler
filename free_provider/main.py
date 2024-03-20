from db import create_tables, drop_tables
from router import router as users_router

from contextlib import asynccontextmanager

from fastapi import FastAPI


# Жизненный цикл приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    await drop_tables()
    print("БД подчищена")
    await create_tables()
    print("и готова к работе!")
    yield
    print("Работа бесплатного провайдера завершена")


app = FastAPI(lifespan=lifespan)
# Подключение роутера для пользователей
app.include_router(users_router)
