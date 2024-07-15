from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

import app.keyboards as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("answer - HI ! ", reply_markup=kb.main)
    await message.reply("reply - HI!")


@router.message(Command("help"))
async def help(message: Message):
    await message.answer("вызов помощи")


@router.message(F.text == "гродно")
async def weather(message: Message):
    await message.answer("погода говно")


@router.message(F.text == "weather")
async def forecast(message: Message):
    await message.answer("выбери период", reply_markup=kb.forecast)


@router.callback_query(F.data == "today")
async def today(callback: CallbackQuery):
    await callback.answer("сегодня")
    await callback.message.answer("прогноз на сегодня")
