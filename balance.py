from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from api import get_balance, transaction

class EditState(StatesGroup):
    edit_balance = State()
    edit_cost = State()

router = Router()

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Можно изменить баланс (/balance), можно изменить расходы (/cost)",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Command("balance"))
async def cmd_start(message: Message, state: FSMContext):    
    current_balance = get_balance(message.from_user.id)
    await message.answer(
        text=f"Текущий баланс: {current_balance}"
    )

@router.message(Command("trans"))
async def cmd_start(message: Message, state: FSMContext):    
    await message.answer(
        text=f"Введите сумму транзакции"
    )
    await state.set_state(EditState.edit_balance)

@router.message(EditState.edit_balance)
async def edit_balance(message: Message, state: FSMContext):
    transaction(user_id=message.from_user.id, value=int(message.text), desc='Test bot transaction')
    await message.answer(
        text="Данные обновлены."
    )
    await state.clear()
