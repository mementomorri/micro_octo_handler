from router import router as free_provider

from fastapi import FastAPI


app = FastAPI(title="Бесплатный провайдер")
app.include_router(free_provider)
