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
    current_balance = api.get_format_balance(message.from_user.id)
    
    await message.answer(text=f"Текущий баланс: {current_balance}")

@router.message(Command("trans"))
async def cmd_trans(message: Message, state: FSMContext):    
    await message.answer(text="Введите сумму транзакции")
    await state.set_state(EditState.edit_balance)

@router.message(EditState.edit_balance)
async def edit_balance(message: Message, state: FSMContext):
    u_id = message.from_user.id
    api.transaction(user_id=u_id, value=int(message.text), desc='Транзакция')
    logger.info(f"Игрок {message.from_user.id} провел транзакцию на {int(message.text)}")
    
    cur_balance = api.get_format_balance(user_id=u_id)
    mes_text = f"Данные обновлены\nТекущий баланс: {cur_balance}"

    await message.answer(text=mes_text)
    await state.clear()
