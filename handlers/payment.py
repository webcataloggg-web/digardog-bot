from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import config
from database import create_order, set_receipt
from keyboards.admin import admin_confirm_keyboard
from keyboards.payment import paid_keyboard, pickup_now_payment_keyboard
from services.cart import clear_cart, get_cart
from states import ReceiptState
from utils.messages import admin_order_text
from utils.telegram import hide_old_buttons


router = Router()

PAYMENT_NAMES = {
    "pay_cash": "Наличными",
    "pay_dc": "DC-bank",
    "pay_alif": "Alif",
    "pay_pickup_later": "При получении",
}

PAYMENT_DETAILS = {
    "pay_dc": "💳 DC-bank:\n17-527-99-55",
    "pay_alif": "🟣 Alif:\n20-22-88-99-9",
}


def build_address(data: dict) -> str | None:
    if data.get("fulfillment") != "Доставка":
        return None
    return (
        f"{data.get('address')}, дом {data.get('house')}, "
        f"подъезд {data.get('entrance')}, квартира {data.get('apartment')}, "
        f"телефон {data.get('phone')}"
    )


async def save_order(message: Message, state: FSMContext, payment_method: str) -> dict | None:
    cart = await get_cart(message.chat.id)
    if not cart:
        await message.answer("🛒 Корзина пуста.")
        await state.clear()
        return None
    data = await state.get_data()
    return await create_order(
        user_id=message.chat.id,
        username=message.chat.username,
        cart=cart,
        fulfillment=data.get("fulfillment", "Самовывоз"),
        payment_method=payment_method,
        address=build_address(data),
    )


async def notify_admin(bot, order: dict, receipt_file_id: str | None = None) -> None:
    text = admin_order_text(order)
    if receipt_file_id:
        await bot.send_photo(
            config.admin_id,
            receipt_file_id,
            caption=text,
            reply_markup=admin_confirm_keyboard(order["order_code"]),
        )
    else:
        await bot.send_message(config.admin_id, text, reply_markup=admin_confirm_keyboard(order["order_code"]))


@router.callback_query(F.data == "pay_pickup_now")
async def pickup_now(callback: CallbackQuery) -> None:
    await callback.answer()
    await hide_old_buttons(callback)
    await callback.message.answer("💰 Способ оплаты:", reply_markup=pickup_now_payment_keyboard())


@router.callback_query(F.data.in_({"pay_cash", "pay_pickup_later"}))
async def pay_without_receipt(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await hide_old_buttons(callback)
    order = await save_order(callback.message, state, PAYMENT_NAMES[callback.data])
    if not order:
        return
    await notify_admin(callback.bot, order)
    await clear_cart(callback.from_user.id)
    await state.clear()
    await callback.message.answer(f"✅ Заказ отправлен админу.\n\n🆔 Номер заказа: {order['order_code']}")


@router.callback_query(F.data.in_({"pay_dc", "pay_alif"}))
async def pay_online(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await hide_old_buttons(callback)
    order = await save_order(callback.message, state, PAYMENT_NAMES[callback.data])
    if not order:
        return
    await state.update_data(order_code=order["order_code"])
    await callback.message.answer(f"{PAYMENT_DETAILS[callback.data]}\n\nПосле оплаты нажмите кнопку ниже.", reply_markup=paid_keyboard())


@router.callback_query(F.data == "pay_paid")
async def paid(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await hide_old_buttons(callback)
    data = await state.get_data()
    if not data.get("order_code"):
        await callback.message.answer("Заказ не найден. Начните заново через /start.")
        await state.clear()
        return
    await state.set_state(ReceiptState.photo)
    await callback.message.answer("📸 Отправьте фото чека оплаты.")


@router.message(ReceiptState.photo, F.photo)
async def receipt_photo(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    order_code = data.get("order_code")
    if not order_code:
        await message.answer("Заказ не найден. Начните заново через /start.")
        await state.clear()
        return
    file_id = message.photo[-1].file_id
    order = await set_receipt(order_code, file_id)
    if not order:
        await message.answer("Заказ не найден. Начните заново через /start.")
        await state.clear()
        return
    await notify_admin(message.bot, order, file_id)
    await clear_cart(message.from_user.id)
    await state.clear()
    await message.answer("✅ Чек получен. Заказ отправлен админу.")


@router.message(ReceiptState.photo)
async def receipt_not_photo(message: Message) -> None:
    await message.answer("❌ Пожалуйста, отправьте фото чека.")
