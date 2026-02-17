from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dishka.integrations.fastapi import setup_dishka
from dishka import make_container

from src.api.ui_router import ui
from src.ioc.providers import AppProvider
from src.utils.get_env import get_db_url
from src.app.lifespan import lifespan

def get_app():
    app = FastAPI(
        lifespan=lifespan
    )
    provider = AppProvider(get_db_url())
    container = make_container(provider)
    setup_dishka(container, app)

    app.mount("/static", StaticFiles(directory="ui"), name="static")

    app.include_router(ui)

    @app.get("/", response_class=HTMLResponse)
    async def main():
        return FileResponse("ui/html/base.html")

    return app


app = get_app()
