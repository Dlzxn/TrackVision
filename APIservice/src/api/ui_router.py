from fastapi import APIRouter
from fastapi.responses import FileResponse

ui = APIRouter(
    prefix="/ui"
)

@ui.get("/registration")
async def get_reg_templ():
    return FileResponse("ui/html/registration.html")


@ui.get("/login")
async def get_login_templ():
    return FileResponse("ui/html/enter.html")