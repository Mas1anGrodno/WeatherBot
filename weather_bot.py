from app.handlers import router
from aiogram import Bot, Dispatcher
import asyncio
import environ
from pathlib import Path
env = environ.Env()
environ.Env.read_env(env_file=Path('./env/.env.dev'))


async def main():
    bot = Bot(token="****************************")
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот Потух")
