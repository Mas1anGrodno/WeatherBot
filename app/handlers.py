from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
import requests, json
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from get_weather import get_weather

router = Router()


class Register(StatesGroup):
    city_name = State()


@router.message(CommandStart())
async def start_command(message: types.Message):
    # await message.answer("answer - HI ! ", reply_markup=kb.main)
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды")


@router.message(Command("help"))
async def help(message: Message):
    await message.answer("вызов помощи")


@router.message(Command("get_weather"))
async def get_weather(message: Message):

    # await message.answer("погода говно")
    x = get_weather(Register.city_name)
    await message.reply(x)


@router.message(Command("weather"))
async def weather(message: Message, state: FSMContext):
    await state.set_state(Register.city_name)
    await message.answer("Введите город")
    # await message.answer("выбери период", reply_markup=kb.forecast)


@router.message(Register.city_name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(city_name=message.text)


"""@router.callback_query(F.data == "today")
async def today(callback: CallbackQuery):
    await callback.answer("сегодня")
    await callback.message.answer("прогноз на сегодня")
"""
