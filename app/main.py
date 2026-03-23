"""Инициализация FastAPI app"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.routers.base import router as base_router
from app.routers.orders import router as orders_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(base_router)
app.include_router(orders_router)
