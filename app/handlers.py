from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
import requests, json
import app.keyboards as kb
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# from get_weather import get_weather

router = Router()


class City(StatesGroup):
    name = State()


@router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("Привет! это тестовый бот OpenWeatherMap ", reply_markup=kb.main)


@router.message(Command("city"))
async def city(message: Message, state: FSMContext):
    await state.set_state(City.name)
    await message.answer("Введите город")


@router.message(City.name)
async def set_city_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    await message.answer(f"выбран город: {data["name"]}")
    
    api_key = "3efb07367c44620fb67d99e607fca049"

    coord_by_name = f"http://api.openweathermap.org/geo/1.0/direct?q={data["name"]},BY&limit=1&appid={api_key}"
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
