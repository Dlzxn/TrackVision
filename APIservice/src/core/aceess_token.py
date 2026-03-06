import os
import datetime

import jwt


def create_access_token(data: dict[str, str]) -> str:
    exp = datetime.datetime.utcnow() + datetime.timedelta(
        days=int(os.getenv("JWT_EXPIRE_DAYS"))
    )

    to_encode = data.copy()
    to_encode.update({"exp": exp})

    return jwt.encode(
        to_encode, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("JWT_ALGORITHM")
    )
