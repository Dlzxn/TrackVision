from fastapi import APIRouter
from fastapi.responses import FileResponse

ui = APIRouter(
    prefix="/ui"
)

@ui.get("/registration")
async def get_reg_templ():
    FileResponse("ui/html/registration.html")