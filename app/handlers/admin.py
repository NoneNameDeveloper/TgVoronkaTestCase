from pyrogram.types import Message

from loader import app

from pyrogram import filters

from app.engine.db.service import get_today_users


@app.on_message(filters.me & filters.command("users_today", prefixes="/"))
async def get_users_count_handler(_, message: Message):
    """функция админа для получения людей, зарегистрированных сегодня"""
    users = await get_today_users()

    return await message.reply(f"Количество пользователей сегодня: {str(len(users))}")
