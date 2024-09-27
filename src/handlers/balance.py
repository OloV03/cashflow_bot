from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from logger import Logger
from api import Api

class EditState(StatesGroup):
    edit_balance = State()
    edit_cost = State()

class EditCashFlowState(StatesGroup):
    edit_cashflow = State()

router = Router()
logger = Logger()
api = Api()

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Список доступных команд есть в выпадающем меню",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Command("balance"))
async def cmd_balance(message: Message):    
    current_balance = api.get_balance(message.from_user.id)
    
    await message.answer(text=f"Текущий баланс: {current_balance}")

@router.message(Command("cashflow"))
async def cmd_cashflow(message: Message, state: FSMContext):    
    current_cashflow = api.get_cashflow(message.from_user.id)
    text = (f"День CashFlow, поступило {current_cashflow}" 
            if current_cashflow >=0 
            else f"День CashFlow, списалось {current_cashflow}")
    
    api.transaction(message.from_user.id, current_cashflow, 'CashFlow Day')
    logger.info(f"Игрок {message.from_user.id} получил {current_cashflow} - CashFlow")
    
    await message.answer(text=text)

@router.message(Command("trans"))
async def cmd_trans(message: Message, state: FSMContext):    
    await message.answer(text="Введите сумму транзакции")
    await state.set_state(EditState.edit_balance)

@router.message(EditState.edit_balance)
async def edit_balance(message: Message, state: FSMContext):
    api.transaction(user_id=message.from_user.id, value=int(message.text), desc='Test bot transaction')
    logger.info(f"Игрок {message.from_user.id} провел транзакцию на {int(message.text)}")
    
    await message.answer(text="Данные обновлены")
    await state.clear()

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
