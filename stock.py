from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from api import get_balance, transaction

class EditState(StatesGroup):
    choose_stock = State()
    edit_sum = State()

router = Router()

def get_stocks_keyboard():
    """ Keyboard with stocks buttons """
    buttons = [
        [
            InlineKeyboardButton(text='GRO4', callback_data='GR'),
            InlineKeyboardButton(text='OK2U', callback_data='OK')
        ],
        [
            InlineKeyboardButton(text='ON2U', callback_data='ON'),
            InlineKeyboardButton(text='MYT4', callback_data='MY')
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

@router.message(Command(commands=["stock"]))
async def cmd_stock(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Выберите акции",
        reply_markup=get_stocks_keyboard()
    )

@router.callback_query(lambda x: F.data in ['GR', 'OK', 'ON', 'MY'])
async def cmd_enter_sum(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=f"Укажите количество акций для покупки"
    )
    await state.set_state(EditState.edit_sum)
    await callback.answer()

@router.message(EditState.edit_sum)
async def edit_balance(message: Message):
    sum_text = int(message.text)
    
    await message.answer(text=f"Кол-во для покупки: {sum_text}")
