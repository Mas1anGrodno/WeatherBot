from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
import requests, json
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import requests, json
import app.keyboards as kb

# from get_weather import get_weather

router = Router()


class Register(StatesGroup):
    city_name = State()


@router.message(CommandStart())
async def start_command(message: types.Message):
    # await message.answer("answer - HI ! ", reply_markup=kb.main)
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды", reply_markup=kb.main)


@router.message(Command("help"))
async def help(message: Message):
    await message.answer("вызов помощи")


@router.message(Command("set_city"))
async def weather(message: Message, state: FSMContext):
    await state.set_state(Register.city_name)
    await message.answer("Введите город")
    # await message.answer("выбери период", reply_markup=kb.forecast)


@router.message(Register.city_name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(city_name=message.text)
    data = await state.get_data()
    await message.answer(f"город сохранен - {data["city_name"]}")


@router.message(Command("get_weather"))
async def get_weather(message: Message):
    # Enter your API key here
    api_key = "3efb07367c44620fb67d99e607fca049"

    # city_name = input("Enter city name : ")

    coord_by_name = f"http://api.openweathermap.org/geo/1.0/direct?q={Register.city_name},BY&limit=1&appid={api_key}"
    get_coord = requests.get(coord_by_name)
    coord = get_coord.json()
    lat = coord[0]["lat"]
    lon = coord[0]["lon"]
    city_name_from_json = coord[0]["name"]

    base_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=hourly,daily,minutely&units=metric&lang=ru&appid={api_key}"
    overview_url = f"https://api.openweathermap.org/data/3.0/onecall/overview?lat={lat}&lon={lon}&units=metric&lang=ru&appid={api_key}"

    response = requests.get(base_url)
    x = response.json()
    overview = requests.get(overview_url)
    j = overview.json()

    y = x["current"]
    z = y["weather"]

    current_temperature = y["temp"]
    current_pressure = y["pressure"]
    current_humidity = y["humidity"]
    weather_description = z[0]["description"]
    weather_overview = j["weather_overview"]
    combine_response = print

    await message.answer(
        f"Температура - {current_temperature}\nДавление - {current_pressure}\nВлажность - {current_humidity}\nСейчас - {weather_description}\n\n{weather_overview}"
    )
    # await message.answer("погода говно")


"""@router.callback_query(F.data == "today")
async def today(callback: CallbackQuery):
    await callback.answer("сегодня")
    await callback.message.answer("прогноз на сегодня")
"""
