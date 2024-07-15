import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router

# name - mas1an_openweather_bot // user mas1an_openweather_bot
# TM link - https://t.me/mas1an_openweather_bot
# token - 6601993688:AAHe_NLDIFoL_A2JyDV_lDIrWrRpLo7qQKA


async def main():
    bot = Bot(token="6601993688:AAHe_NLDIFoL_A2JyDV_lDIrWrRpLo7qQKA")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот Потух")
