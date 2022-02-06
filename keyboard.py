from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


settings = KeyboardButton('⚙ Settings')
manual = KeyboardButton('📜 Manual')

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(settings, manual)

