from router import router as users_router

from fastapi import FastAPI


app = FastAPI(title="paid_provider")
app.include_router(users_router)
