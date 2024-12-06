from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery, Location
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from .get_weather import weather_now, weather_overview, weather_hourly, weather_three_days

router = Router()


class City(StatesGroup):
    city_name = State()
    country_name = State()
    forecast = State()
    lat = State()
    lon = State()


@router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer('Привет! это бот OpenWeatherMap.\n Что-бы начать, нажми кнопку "Узнать погоду".', reply_markup=kb.main)


@router.message(F.location)
async def handle_location(message: types.Message, state: FSMContext):
    await state.update_data(lat=message.location.latitude, lon=message.location.longitude, city_name=None, country_name=None)
    await message.answer("Выбери прогноз", reply_markup=kb.chose_forecast)


@router.message(F.text == "Узнать погоду")
async def get_country(message: Message, state: FSMContext):
    await state.update_data(city_name=None, country_name=None, forecast=None, lat=None, lon=None)
    await state.set_state(City.country_name)
    await message.answer("Выбери страну", reply_markup=kb.chose_country)


@router.callback_query(City.country_name)
async def set_country(callback: CallbackQuery, state: FSMContext):
    if callback.data == "by":
        await callback.answer("Вы выбрали Беларусь")
    else:
        await callback.answer("Вы выбрали Россия")
    await state.update_data(country_name=callback.data, lat=None, lon=None)  # Очистка координат
    await state.set_state(City.city_name)
    await callback.message.answer("Введите город")


@router.message(City.city_name)
async def get_forecast(message: Message, state: FSMContext):
    await state.update_data(city_name=message.text)
    await state.set_state(City.forecast)
    await message.answer("Выбери прогноз", reply_markup=kb.chose_forecast)


@router.message(City.forecast)
async def send_forecast(message: Message, state: FSMContext):
    try:
        await state.update_data(forecast=message.text)
        data = await state.get_data()

        if data["forecast"] == "Сегодня":
            await message.answer(
                weather_now(
                    city_name=data["city_name"],
                    country_name=data["country_name"],
                    lat=data["lat"],
                    lon=data["lon"],
                )
            )

        elif data["forecast"] == "На ближайшее время":
            await message.answer(
                weather_hourly(
                    city_name=data["city_name"],
                    country_name=data["country_name"],
                    lat=data["lat"],
                    lon=data["lon"],
                )
            )

        elif data["forecast"] == "Описание":
            await message.answer(
                weather_overview(
                    city_name=data["city_name"],
                    country_name=data["country_name"],
                    lat=data["lat"],
                    lon=data["lon"],
                )
            )

        elif data["forecast"] == "На три дня":
            await message.answer(
                weather_three_days(
                    city_name=data["city_name"],
                    country_name=data["country_name"],
                    lat=data["lat"],
                    lon=data["lon"],
                )
            )

        # await message.answer("Посмторим погоду еще где-нибудь ?", reply_markup=kb.main)
        await message.answer("Другой прогноз", reply_markup=kb.chose_forecast)

    except IndexError:
        await message.answer("Такой город не найден", reply_markup=kb.main)
