from datetime import datetime

from pydantic import BaseModel


class ChatData(BaseModel):
    message: str
    timestamp: datetime