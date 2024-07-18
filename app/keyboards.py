from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Узнать погоду")]], resize_keyboard=True, input_field_placeholder="Давай узнаем погоду :)")

chose_country = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Беларусь", callback_data="by")], [InlineKeyboardButton(text="Россия", callback_data="ru")]])

chose_forecast = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Краткий")], [KeyboardButton(text="Развернутый")]], resize_keyboard=True)
