from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from logger import info
from api import get_balance, transaction, get_cashflow, set_cashflow

class EditState(StatesGroup):
    edit_balance = State()
    edit_cost = State()

class EditCashFlowState(StatesGroup):
    edit_cashflow = State()

router = Router()

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Список доступных команд есть в выпадающем меню",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Command("balance"))
async def cmd_balance(message: Message):    
    current_balance = get_balance(message.from_user.id)
    
    await message.answer(text=f"Текущий баланс: {current_balance}")

@router.message(Command("cashflow"))
async def cmd_balance(message: Message, state: FSMContext):    
    current_cashflow = get_cashflow(message.from_user.id)
    text = (f"День CashFlow, поступило {current_cashflow}" 
            if current_cashflow >=0 
            else f"День CashFlow, списалось {current_cashflow}")
    
    transaction(message.from_user.id, current_cashflow, 'CashFlow Day')
    info(f"Игрок {message.from_user.id} получил {current_cashflow} - CashFlow")
    
    await message.answer(text=text)

@router.message(Command("trans"))
async def cmd_trans(message: Message, state: FSMContext):    
    await message.answer(text=f"Введите сумму транзакции")
    await state.set_state(EditState.edit_balance)

@router.message(EditState.edit_balance)
async def edit_balance(message: Message, state: FSMContext):
    transaction(user_id=message.from_user.id, value=int(message.text), desc='Test bot transaction')
    info(f"Игрок {message.from_user.id} провел транзакцию на {int(message.text)}")
    
    await message.answer(text="Данные обновлены")
    await state.clear()

@router.message(Command("new_cashflow"))
async def cmd_trans(message: Message, state: FSMContext):    
    await message.answer(text=f"Введите новое значение CashFlow")
    await state.set_state(EditCashFlowState.edit_cashflow)

@router.message(EditCashFlowState.edit_cashflow)
async def edit_balance(message: Message, state: FSMContext):
    set_cashflow(user_id=message.from_user.id, cashflow=int(message.text))
    info(f"Игрок {message.from_user.id} обновил значение CashFlow : {int(message.text)}")
    
    await message.answer(text="Данные обновлены")
    await state.clear()
