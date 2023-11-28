import os.path
from dataclasses import dataclass
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict


@dataclass
class VoronkaModel:
    sleep: int  # задержка после последнего сообщения
    content_type: str  # тип данных этой части
    content: str  # содержимое части
    condition: str  # условие при котором срабатывает эта часть


@dataclass
class VoronkaSettings:
    data = {
        "settings": [
            {
                "sleep": 0,
                "content_type": "text",
                "content": "Добрый день!"
            },
            {
                "sleep": 0,
                "content_type": "text",
                "content": "Подготовила для вас материал"
            },
            {
                "sleep": 0,
                "content_type": "photo",
                "content": "https://cdn.pixabay.com/photo/2017/07/25/01/22/cat-2536662_640.jpg"
            },
            {
                "sleep": 0,
                "content_type": "text",
                "content": "Скоро вернусь с новым материалом!",
                "condition": "trigger"
            }
        ]
    }

    def to_model(cls) -> list[VoronkaModel]:
        """возвращаем словарь с настройками в обьекте python (модели)"""
        return [
            VoronkaModel(
                sleep=d["sleep"],
                content_type=d["content_type"],
                content=d["content"],
                condition=d["condition"] if "condition" in d.keys() else None) for d in cls.data["settings"]
        ]


class Settings(BaseSettings):
    API_ID: int
    API_HASH: str

    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int | str

    TRIGGER: ClassVar

    CONNECTION_STRING: ClassVar  # connection to db string

    env_path: ClassVar = os.path.abspath(".env")
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding='utf-8')


Settings.TRIGGER = "Хорошего дня"
Settings.CONNECTION_STRING = f"postgresql+asyncpg://{Settings().DB_USERNAME}:{Settings().DB_PASSWORD}@{Settings().DB_HOST}:{Settings().DB_PORT}/{Settings().DB_NAME}"