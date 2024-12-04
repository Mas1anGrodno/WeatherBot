from app.handlers import router
from aiogram import Bot, Dispatcher
import asyncio
import environ
from pathlib import Path

env = environ.Env()
environ.Env.read_env(env_file=Path("./env/.env.dev"))

BOT_SECRET_KEY = env("BOT_SECRET_KEY")


async def main():
    bot = Bot(token=BOT_SECRET_KEY)
    dp = Dispatcher()
    dp.include_router(router)
    print("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
