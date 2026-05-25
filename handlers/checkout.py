from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.payment import delivery_payment_keyboard, pickup_when_keyboard
from states import DeliveryState
from utils.telegram import hide_old_buttons


router = Router()


@router.callback_query(F.data == "delivery_start")
async def start_delivery(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await hide_old_buttons(callback)
    await state.update_data(fulfillment="Доставка")
    await state.set_state(DeliveryState.address)
    await callback.message.answer("🚚 Доставка\n\nВведите адрес:")


@router.message(DeliveryState.address)
async def delivery_address(message: Message, state: FSMContext) -> None:
    await state.update_data(address=message.text)
    await state.set_state(DeliveryState.house)
    await message.answer("Введите дом:")


@router.message(DeliveryState.house)
async def delivery_house(message: Message, state: FSMContext) -> None:
    await state.update_data(house=message.text)
    await state.set_state(DeliveryState.entrance)
    await message.answer("Введите подъезд:")


@router.message(DeliveryState.entrance)
async def delivery_entrance(message: Message, state: FSMContext) -> None:
    await state.update_data(entrance=message.text)
    await state.set_state(DeliveryState.apartment)
    await message.answer("Введите квартиру:")


@router.message(DeliveryState.apartment)
async def delivery_apartment(message: Message, state: FSMContext) -> None:
    await state.update_data(apartment=message.text)
    await state.set_state(DeliveryState.phone)
    await message.answer("Введите телефон:")


@router.message(DeliveryState.phone)
async def delivery_phone(message: Message, state: FSMContext) -> None:
    await state.update_data(phone=message.text)
    await message.answer("💰 Способ оплаты:", reply_markup=delivery_payment_keyboard())


@router.callback_query(F.data == "delivery_pickup")
async def pickup(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await hide_old_buttons(callback)
    await state.update_data(fulfillment="Самовывоз", address=None)
    await callback.message.answer("💰 Когда оплатите?", reply_markup=pickup_when_keyboard())
