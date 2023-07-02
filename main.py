import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
import handlers
from config import TOKEN


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(handlers.router)

    await bot.set_my_commands([BotCommand(command='start', description='Старт')])
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    asyncio.run(main())
