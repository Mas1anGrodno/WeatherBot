from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="гродно")], [KeyboardButton(text="Привет")], [KeyboardButton(text="/help"), KeyboardButton(text="weather")]],
    resize_keyboard=True,
    input_field_placeholder="жми кнопку",
)

forecast = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="today", callback_data="today")],
        [InlineKeyboardButton(text="3 days", callback_data="three_dys")],
        [InlineKeyboardButton(text="7 days", callback_data="seven_dys")],
    ]
)
