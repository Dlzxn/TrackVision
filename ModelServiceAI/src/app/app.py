from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from src.api.socker_router import socket
from src.ioc.YoLo_provider import AIProvider
from src.app.lifespan import lifespan


def create_app():
    app = FastAPI(
        title="API",
        version="0.0.1",
        lifespan=lifespan,
    )

    container = make_async_container(AIProvider())
    setup_dishka(container, app)

    app.include_router(socket)
    return app

app = create_app()