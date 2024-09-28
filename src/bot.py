from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import bot_token
import handlers.stock as stock
from handlers.cashflow import router as cashflow_router
from handlers.balance import router as balance_router

async def run_bot():

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(bot_token)

    dp.include_router(balance_router)
    dp.include_router(cashflow_router)
    dp.include_router(stock.router)
    await dp.start_polling(bot)
