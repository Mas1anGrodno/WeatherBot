from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery, Location
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from get_weather import get_weather, get_weather_overview, get_weather_by_coord, get_weather_overview_by_coord

router = Router()


class City(StatesGroup):
    name = State()
    country = State()
    forecast = State()
    lat = State()
    lon = State()

@router.message(F.location)
async def handle_location(message: types.Message):
    print('function started')
    City.lat = message.location.latitude
    City.lon = message.location.longitude
    await message.answer("Выбери прогноз", reply_markup=kb.chose_forecast_by_coord)

@router.message(F.text.in_({"Коротко", "Развернуто"}))
async def handle_forecast(message: types.Message):
    if message.text == "Коротко":
        await message.answer(get_weather_by_coord(City.lat, City.lon))
    elif message.text == "Развернуто":
        await message.answer(get_weather_overview_by_coord(City.lat, City.lon))  
    await message.answer("Посмторим погоду еще где-нибудь ?", reply_markup=kb.main)

@router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer("Привет! это бот OpenWeatherMap.\n Что-бы начать, нажми кнопку \"Узнать погоду\".", reply_markup=kb.main)



@router.message(F.text == "Узнать погоду")
async def get_country(message: Message, state: FSMContext):
    await state.set_state(City.country)
    await message.answer("Выбери страну", reply_markup=kb.chose_country)


@router.callback_query(City.country)
async def set_country(callback: CallbackQuery, state: FSMContext):
    if callback.data == "by":
        await callback.answer("Вы выбрали Беларусь")
    else:
        await callback.answer("Вы выбрали Россия")
    await state.update_data(country=callback.data)
    await state.set_state(City.name)
    await callback.message.answer("Введите город")


@router.message(City.name)
async def get_forecast(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(City.forecast)
    await message.answer("Выбери прогноз", reply_markup=kb.chose_forecast)


@router.message(City.forecast)
async def send_forecast(message: Message, state: FSMContext):
    try:
        await state.update_data(forecast=message.text)
        data = await state.get_data()
        if data["forecast"] == "Краткий":
            await message.answer(get_weather(data["name"], data["country"]))
            await message.answer("Посмторим погоду еще где-нибудь ?", reply_markup=kb.main)
        else:
            await message.answer(get_weather_overview(data["name"], data["country"]))
            await message.answer("Посмторим погоду еще где-нибудь ?", reply_markup=kb.main)

    except IndexError:
        await message.answer("Такой город не найден", reply_markup=kb.main)

