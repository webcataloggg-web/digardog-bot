from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery


async def hide_old_buttons(callback: CallbackQuery) -> None:
    if not callback.message:
        return
    try:
        await callback.message.edit_reply_markup(reply_markup=None)
    except TelegramBadRequest:
        pass
