from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.menu import categories_keyboard
from utils.messages import WELCOME_TEXT


router = Router()


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(WELCOME_TEXT, reply_markup=categories_keyboard())
