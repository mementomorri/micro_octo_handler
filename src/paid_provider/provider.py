from router import router as paid_provider

from fastapi import FastAPI


app = FastAPI(title="Платный провайдер")
app.include_router(paid_provider)
