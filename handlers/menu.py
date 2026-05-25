from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.menu import categories_keyboard, category_keyboard, product_keyboard
from services.cart import change_selected_qty, get_selected_qty, set_selected_qty
from services.catalog import PRODUCTS, get_category
from utils.messages import WELCOME_TEXT
from utils.telegram import hide_old_buttons


router = Router()


@router.callback_query(F.data == "category_back")
async def back_to_categories(callback: CallbackQuery) -> None:
    await callback.answer()
    await hide_old_buttons(callback)
    await callback.message.answer(WELCOME_TEXT, reply_markup=categories_keyboard())


@router.callback_query(F.data.startswith("category_") & (F.data != "category_back"))
async def show_category(callback: CallbackQuery) -> None:
    await callback.answer()
    await hide_old_buttons(callback)
    category_id = callback.data.removeprefix("category_")
    category = get_category(category_id)
    if not category:
        await callback.message.answer("Категория не найдена.", reply_markup=categories_keyboard())
        return
    await callback.message.answer(f"{category.title}\n\nВыберите товар:", reply_markup=category_keyboard(category_id))


@router.callback_query(F.data.startswith("add_select_"))
async def select_product(callback: CallbackQuery) -> None:
    await callback.answer()
    await hide_old_buttons(callback)
    product_id = callback.data.removeprefix("add_select_")
    product = PRODUCTS.get(product_id)
    if not product:
        await callback.message.answer("Товар не найден.", reply_markup=categories_keyboard())
        return
    qty = await set_selected_qty(callback.from_user.id, product_id, 1)
    await callback.message.answer(
        f"{product.name}\n\n💰 Цена: {product.price} смн\n\nВыберите количество:",
        reply_markup=product_keyboard(product, qty),
    )


@router.callback_query(F.data.startswith("qty_plus_"))
async def plus_qty(callback: CallbackQuery) -> None:
    await callback.answer()
    product_id = callback.data.removeprefix("qty_plus_")
    product = PRODUCTS.get(product_id)
    if not product:
        return
    qty = await change_selected_qty(callback.from_user.id, product_id, 1)
    await callback.message.edit_reply_markup(reply_markup=product_keyboard(product, qty))


@router.callback_query(F.data.startswith("qty_minus_"))
async def minus_qty(callback: CallbackQuery) -> None:
    await callback.answer()
    product_id = callback.data.removeprefix("qty_minus_")
    product = PRODUCTS.get(product_id)
    if not product:
        return
    qty = await change_selected_qty(callback.from_user.id, product_id, -1)
    await callback.message.edit_reply_markup(reply_markup=product_keyboard(product, qty))


@router.callback_query(F.data.startswith("qty_show_"))
async def show_qty(callback: CallbackQuery) -> None:
    await callback.answer("Количество")
