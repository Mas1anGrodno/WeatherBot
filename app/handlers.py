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


@router.message(F.location)
async def handle_location(message: types.Message, state: FSMContext):
    await state.update_data(lat=message.location.latitude, lon=message.location.longitude)
    await message.answer("Выбери прогноз", reply_markup=kb.chose_forecast)


@router.message(F.text.in_({"Сегодня", "На ближайшее время", "Описание", "На три дня"}))
async def handle_forecast(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == "Сегодня":
        if "lat" in data and "lon" in data:
            await message.answer(weather_now(lat=data["lat"], lon=data["lon"]))
    elif message.text == "На ближайшее время":
        if "lat" in data and "lon" in data:
            await message.answer(weather_hourly(lat=data["lat"], lon=data["lon"]))
    elif message.text == "Описание":
        if "lat" in data and "lon" in data:
            await message.answer(weather_overview(lat=data["lat"], lon=data["lon"]))
    elif message.text == "На три дня":
        if "lat" in data and "lon" in data:
            await message.answer(weather_three_days(lat=data["lat"], lon=data["lon"]))
    await message.answer("Посмторим погоду еще где-нибудь ?", reply_markup=kb.main)


@router.message(F.text == "Узнать погоду")
async def get_country(message: Message, state: FSMContext):
    await state.clear()  # Очистка состояния
    await state.set_state(City.country_name)
    await message.answer("Выбери страну", reply_markup=kb.chose_country)


@router.callback_query(City.country_name)
async def set_country(callback: CallbackQuery, state: FSMContext):
    await state.update_data(country_name=callback.data, lat=None, lon=None)  # Очистка координат
    if callback.data == "by":
        await callback.answer("Вы выбрали Беларусь")
    else:
        await callback.answer("Вы выбрали Россия")
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
            await message.answer(weather_now(city_name=data["city_name"], country_name=data["country_name"]))
        elif data["forecast"] == "На ближайшее время":
            await message.answer(weather_hourly(city_name=data["city_name"], country_name=data["country_name"]))
        elif data["forecast"] == "Описание":
            await message.answer(weather_overview(city_name=data["city_name"], country_name=data["country_name"]))
        elif data["forecast"] == "На три дня":
            await message.answer(weather_three_days(city_name=data["city_name"], country_name=data["country_name"]))
        await message.answer("Посмторим погоду еще где-нибудь ?", reply_markup=kb.main)
    except IndexError:
        await message.answer("Такой город не найден", reply_markup=kb.main)


# -------------------------------OLD-------------------------------------------------

# @router.message(F.location)
# async def handle_location(message: types.Message):
#     City.lat = message.location.latitude
#     City.lon = message.location.longitude
#     await message.answer("Выбери прогноз", reply_markup=kb.chose_forecast)

# @router.message(F.text.in_({"Сегодня", "На ближайшее время", "Описание", "На три дня"}))
# async def handle_forecast(message: types.Message):
#     if message.text == "Сегодня":
#         await message.answer(weather_now(lat=City.lat, lon=City.lon))
#     elif message.text == "На ближайшее время":
#         await message.answer(weather_hourly(lat=City.lat, lon=City.lon))
#     elif message.text == "Описание":
#         await message.answer(weather_overview(lat=City.lat, lon=City.lon))
#     elif message.text == "На три дня":
#         await message.answer(weather_three_days(lat=City.lat, lon=City.lon))
#     await message.answer("Посмторим погоду еще где-нибудь ?", reply_markup=kb.main)


# @router.message(CommandStart())
# async def start_command(message: types.Message):
#     await message.answer('Привет! это бот OpenWeatherMap.\n Что-бы начать, нажми кнопку "Узнать погоду".', reply_markup=kb.main)


# @router.message(F.text == "Узнать погоду")
# async def get_country(message: Message, state: FSMContext):
#     await state.set_state(City.country_name)
#     await message.answer("Выбери страну", reply_markup=kb.chose_country)


# @router.callback_query(City.country_name)
# async def set_country(callback: CallbackQuery, state: FSMContext):
#     if callback.data == "by":
#         await callback.answer("Вы выбрали Беларусь")
#     else:
#         await callback.answer("Вы выбрали Россия")
#     await state.update_data(country_name=callback.data)
#     await state.set_state(City.city_name)
#     await callback.message.answer("Введите город")


# @router.message(City.city_name)
# async def get_forecast(message: Message, state: FSMContext):
#     await state.update_data(city_name=message.text)
#     await state.set_state(City.forecast)
#     await message.answer("Выбери прогноз", reply_markup=kb.chose_forecast)


# @router.message(City.forecast)
# async def send_forecast(message: Message, state: FSMContext):
#     try:
#         await state.update_data(forecast=message.text)
#         data = await state.get_data()
#         if data["forecast"] == "Сегодня":
#             await message.answer(weather_now(city_name=data["city_name"], country_name=data["country_name"]))
#             await message.answer("Посмторим погоду еще где-нибудь ?", reply_markup=kb.main)

#         elif data["forecast"] == "На ближайшее время":
#             await message.answer(weather_hourly(city_name=data["city_name"], country_name=data["country_name"]))
#             await message.answer("Посмторим погоду еще где-нибудь ?", reply_markup=kb.main)

#         elif data["forecast"] == "Описание":
#             await message.answer(weather_overview(city_name=data["city_name"], country_name=data["country_name"]))
#             await message.answer("Посмторим погоду еще где-нибудь ?", reply_markup=kb.main)

#         elif data["forecast"] == "На три дня":
#             await message.answer(weather_three_days(city_name=data["city_name"], country_name=data["country_name"]))
#             await message.answer("Посмторим погоду еще где-нибудь ?", reply_markup=kb.main)

#     except IndexError:
#         await message.answer("Такой город не найден", reply_markup=kb.main)
