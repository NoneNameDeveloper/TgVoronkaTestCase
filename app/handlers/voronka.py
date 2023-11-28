from pyrogram import filters, types

from app.engine.db.service import registrate_user

from app.engine.logic.misc import process

from loader import app


@app.on_message(filters.text & filters.private & ~filters.me)
async def get_messages_handler(_, message: types.Message):

    # user registration
    new_user: bool = await registrate_user(
        message.chat.id,
        message.from_user.first_name,
        message.from_user.last_name
    )

    if new_user:
        return await process(message)

    else:
        pass