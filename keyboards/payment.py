from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def delivery_payment_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💵 Наличными", callback_data="pay_cash")],
            [InlineKeyboardButton(text="💳 DC-bank", callback_data="pay_dc")],
            [InlineKeyboardButton(text="🟣 Alif", callback_data="pay_alif")],
        ]
    )


def pickup_when_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 Сейчас", callback_data="pay_pickup_now")],
            [InlineKeyboardButton(text="💵 При получении", callback_data="pay_pickup_later")],
        ]
    )


def pickup_now_payment_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💳 DC-bank", callback_data="pay_dc")],
            [InlineKeyboardButton(text="🟣 Alif", callback_data="pay_alif")],
        ]
    )


def paid_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="✅ Оплатил", callback_data="pay_paid")]])
