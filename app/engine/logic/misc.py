import asyncio
import traceback

from pyrogram import types

from app.data.config import VoronkaModel, VoronkaSettings, Settings
from loader import app

from loguru import logger


async def process(message: types.Message):
    """process main logic of tornado (voronka)"""

    voronka_model: list[VoronkaModel] = VoronkaSettings().to_model()

    # перебираем все шаги воронки
    for step in voronka_model:
        if step.sleep and step.sleep > 0:
            await asyncio.sleep(step.sleep * 60)

        if step.condition:
            if step.condition == "trigger":
                # триггер был - выходим
                trigger_exists = await check_trigger(message.chat.id)

                if trigger_exists:
                    return "Finish"

                # триггера не было, прощание
                else:
                    await app.send_message(message.chat.id, "Скоро вернусь с новым материалом!")
                    logger.info(f"Сообщение отправлено {message.chat.id} | '{step.content}'")
                    return "Finish"

        # фотография
        if step.content_type == "photo":
            try:
                await app.send_photo(message.chat.id, step.content)
                logger.info(f"Сообщение отправлено {message.chat.id} | '{step.content}'")
            except Exception as e:
                logger.exception(str(traceback.format_exc()))

        # текст
        elif step.content_type == "text":
            try:
                await app.send_message(message.chat.id, step.content)
                logger.info(f"Сообщение отправлено {message.chat.id} | '{step.content}'")
            except Exception as e:
                logger.exception(str(traceback.format_exc()))

        # неподдерживаемый тип данных
        else:
            logger.error(f"Content type of content: '{step.content}' not supported!")

    return "Finish"


async def check_trigger(chat_id: int) -> bool:
    """check if trigger exists in all messages in chat"""
    async for message in app.get_chat_history(chat_id=chat_id):
        message: types.Message

        # получаем текст с сообщения (если он есть, под картинкой или просто)
        text = message.text or message.caption or ""

        # проверяем на вхождение триггера в текст
        if (message.from_user.id == app.me.id) and (Settings.TRIGGER.lower() in text.lower().strip()):
            return True

    return False