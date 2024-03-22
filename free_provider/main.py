from router import router as free_provider

from fastapi import FastAPI


app = FastAPI(title="free_provider")
app.include_router(free_provider)
