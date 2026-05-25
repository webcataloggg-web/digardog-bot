from aiogram.fsm.state import State, StatesGroup


class DeliveryState(StatesGroup):
    address = State()
    house = State()
    entrance = State()
    apartment = State()
    phone = State()


class ReceiptState(StatesGroup):
    photo = State()
