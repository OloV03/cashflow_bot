from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import bot_token
import handlers.balance as balance
import handlers.stock as stock

async def run_bot():

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(bot_token)

    dp.include_router(balance.router)
    dp.include_router(stock.router)
    await dp.start_polling(bot)
