from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.menu import categories_keyboard, continue_keyboard, fulfillment_keyboard
from services.cart import add_to_cart, get_cart, get_selected_qty
from services.catalog import PRODUCTS
from utils.messages import WELCOME_TEXT, order_summary
from utils.telegram import hide_old_buttons


router = Router()


@router.callback_query(F.data.startswith("add_cart_"))
async def add_product_to_cart(callback: CallbackQuery) -> None:
    await callback.answer()
    await hide_old_buttons(callback)
    product_id = callback.data.removeprefix("add_cart_")
    if product_id not in PRODUCTS:
        await callback.message.answer("Товар не найден.", reply_markup=categories_keyboard())
        return
    qty = await get_selected_qty(callback.from_user.id, product_id)
    await add_to_cart(callback.from_user.id, product_id, qty)
    await callback.message.answer("✅ Добавлено в корзину\n\nХотите ещё что-нибудь?", reply_markup=continue_keyboard())


@router.callback_query(F.data == "cart_yes")
async def cart_continue(callback: CallbackQuery) -> None:
    await callback.answer()
    await hide_old_buttons(callback)
    await callback.message.answer(WELCOME_TEXT, reply_markup=categories_keyboard())


@router.callback_query(F.data.in_({"cart_no", "cart_view"}))
async def show_cart(callback: CallbackQuery) -> None:
    await callback.answer()
    await hide_old_buttons(callback)
    cart = await get_cart(callback.from_user.id)
    if not cart:
        await callback.message.answer("🛒 Корзина пуста.", reply_markup=categories_keyboard())
        return
    await callback.message.answer(order_summary(cart), reply_markup=fulfillment_keyboard())
