from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(
    # keyboard=[[KeyboardButton(text="гродно")], [KeyboardButton(text="Привет")], [KeyboardButton(text="/help"), KeyboardButton(text="/weather")]],
    keyboard=[[KeyboardButton(text="/city")], [KeyboardButton(text="/start")]],
    resize_keyboard=True,
    input_field_placeholder="жми кнопку",
)

# chhose_country = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Беларусь", callback_data="by")], [InlineKeyboardButton(text="Россия", callback_data="ru")]])
