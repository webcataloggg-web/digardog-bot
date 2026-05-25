from aiogram import F, Router
from aiogram.types import CallbackQuery

from config import config
from database import get_order_by_code, set_status
from keyboards.admin import admin_ready_keyboard
from utils.messages import confirmed_text
from utils.telegram import hide_old_buttons


router = Router()


def is_admin(user_id: int) -> bool:
    return user_id == config.admin_id


def fulfillment_kind(order: dict) -> str:
    raw_value = order.get("delivery_type") or order.get("fulfillment") or ""
    value = str(raw_value).strip().casefold()
    if value in {"delivery", "доставка", "🚚 доставка"}:
        return "delivery"
    if value in {"pickup", "самовывоз", "🛍 самовывоз"}:
        return "pickup"
    return value


@router.callback_query(F.data.startswith("admin_confirm_"))
async def admin_confirm(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    await callback.answer()
    order_code = callback.data.removeprefix("admin_confirm_")
    order = await set_status(order_code, "confirmed")
    if not order:
        await callback.message.answer("Заказ не найден.")
        return
    await callback.bot.send_message(order["user_id"], confirmed_text(order))
    if fulfillment_kind(order) == "pickup":
        await callback.message.edit_reply_markup(reply_markup=admin_ready_keyboard(order_code))
        return
    await hide_old_buttons(callback)


@router.callback_query(F.data.startswith("admin_reject_"))
async def admin_reject(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    await callback.answer()
    order_code = callback.data.removeprefix("admin_reject_")
    order = await set_status(order_code, "rejected")
    if not order:
        await callback.message.answer("Заказ не найден.")
        return
    await callback.bot.send_message(order["user_id"], "❌ Заказ не принят.\n\n🙏 Простите за неудобства.")
    await hide_old_buttons(callback)


@router.callback_query(F.data.startswith("admin_ready_"))
async def admin_ready(callback: CallbackQuery) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer("Нет доступа", show_alert=True)
        return
    await callback.answer()
    order_code = callback.data.removeprefix("admin_ready_")
    order = await get_order_by_code(order_code)
    if not order:
        await callback.message.answer("Заказ не найден.")
        return
    if fulfillment_kind(order) != "pickup":
        await hide_old_buttons(callback)
        return
    await set_status(order_code, "ready")
    await callback.bot.send_message(order["user_id"], "🛍 Ваш заказ готов!\n\n📍 Можете прийти забрать заказ.")
    await hide_old_buttons(callback)
