from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dishka.integrations.fastapi import setup_dishka
from dishka import make_async_container

from src.api.ui_router import ui
from src.api.api_auth_router import auth_router
from src.ioc.providers import AppProvider
from src.utils.get_env import get_db_url
from src.app.lifespan import lifespan

def get_app():
    app = FastAPI(
        lifespan=lifespan
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    provider = AppProvider(get_db_url())
    container = make_async_container(provider)
    setup_dishka(container, app)

    app.include_router(ui)
    app.include_router(auth_router)

    app.mount("/static", StaticFiles(directory="ui"), name="static")

    @app.get("/", response_class=HTMLResponse)
    async def main():
        return FileResponse("ui/html/base.html")

    return app


app = get_app()
