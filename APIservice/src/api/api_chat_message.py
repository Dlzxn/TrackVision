from fastapi import APIRouter

from .models.message import ChatData


chat_message_router = APIRouter(
    prefix="/chat", tags=["chat message"]
)


@chat_message_router.post('/message')
async def message(chat_data: ChatData):
    return {
        "response": "Hello world!"
    }