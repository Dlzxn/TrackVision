from contextlib import asynccontextmanager
from fastapi import FastAPI
from dishka import AsyncContainer

from src.domain.services.detector import YOLOContract


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: AsyncContainer = app.state.dishka_container
    print("Сервер запущен...")
    await container.get(YOLOContract)
    yield
    print("Сервер остановлен")