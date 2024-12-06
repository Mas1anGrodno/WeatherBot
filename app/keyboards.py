from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Узнать погоду")], [KeyboardButton(text="Узнать погоду по координатам", request_location=True)], [KeyboardButton(text="/start")]],
    resize_keyboard=True,
    input_field_placeholder="Давай узнаем погоду :)",
)

chose_country = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Беларусь", callback_data="by")], [InlineKeyboardButton(text="Россия", callback_data="ru")]],
)


chose_forecast = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Сегодня")], [KeyboardButton(text="На ближайшее время")], [KeyboardButton(text="Описание")], [KeyboardButton(text="На три дня")]],
    resize_keyboard=True,
)
