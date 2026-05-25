from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_confirm_keyboard(order_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"admin_confirm_{order_code}"),
                InlineKeyboardButton(text="❌ Отклонить", callback_data=f"admin_reject_{order_code}"),
            ]
        ]
    )


def admin_ready_keyboard(order_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🛍 Заказ готов", callback_data=f"admin_ready_{order_code}")]]
    )
