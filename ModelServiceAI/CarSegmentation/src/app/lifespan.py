from contextlib import asynccontextmanager
from fastapi import FastAPI
from dishka import AsyncContainer

from src.domain.YoLoContract import YoLoAbstract
from src.domain.OCRcontract import OCRAbstract


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: AsyncContainer = app.state.dishka_container
    print("Сервер запущен...")
    await container.get(YoLoAbstract)
    await container.get(OCRAbstract)
    print("Модели готовы!")
    yield
    print("Сервер остановлен")