from fastapi import FastAPI
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from src.ioc.providersAI import AIProvider
from src.api.socket import socket
from src.app.lifespan import lifespan



def get_app():
    app = FastAPI(
        title="apiV2",
        version="0.0.1",
        lifespan=lifespan
    )
    container = make_async_container(AIProvider())
    setup_dishka(container, app)

    app.include_router(socket)
    return app

app = get_app()