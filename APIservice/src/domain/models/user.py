from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    name: str
    email: str
    password: str
    tg_id: Optional[int]
    tg_username: Optional[str]

    def update_telegram(self, tg_id: int, username: str):
        """Пример метода бизнес-логики"""
        self.tg_id = tg_id
        self.tg_username = username