from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from aiogram import Router
from logger import Logger
from api import Api

class EditCashFlowState(StatesGroup):
    edit_cashflow = State()

router = Router()
logger = Logger()
api = Api()

@router.message(Command("cashflow"))
async def cmd_cashflow(message: Message):  
    u_id = message.from_user.id
    current_cashflow = api.get_cashflow(u_id)

    api.transaction(message.from_user.id, current_cashflow, 'CashFlow Day')
    
    text = (f"День CashFlow, поступило {current_cashflow}" 
            if current_cashflow >=0 
            else f"День CashFlow, списалось {current_cashflow}")
    
    cur_balance = api.get_format_balance(user_id=u_id)
    text = text + f"\nТекущий баланс: {cur_balance}"

    logger.info(f"Игрок {message.from_user.id} получил {current_cashflow} - CashFlow")
    await message.answer(text=text)

@router.message(Command("new_cashflow"))
async def cmd_new_cashflow(message: Message, state: FSMContext):    
    await message.answer(text="Введите новое значение CashFlow")
    await state.set_state(EditCashFlowState.edit_cashflow)

@router.message(EditCashFlowState.edit_cashflow)
async def edit_cashflow(message: Message, state: FSMContext):
    api.set_cashflow(user_id=message.from_user.id, cashflow=int(message.text))
    logger.info(f"Игрок {message.from_user.id} обновил значение CashFlow : {int(message.text)}")
    
    await message.answer(text="Данные обновлены")
    await state.clear()
