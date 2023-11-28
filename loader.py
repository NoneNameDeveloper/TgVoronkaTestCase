from functools import lru_cache

from app.data.config import Settings

from pyrogram import Client

import loguru


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()

app = Client(
    "client",
    api_id=settings.API_ID,
    api_hash=settings.API_HASH
)

