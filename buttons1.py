from telebot import types

def phone_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton("📱 Поделиться номером", request_contact=True)
    kb.add(button)
    return kb

def location_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = types.KeyboardButton("📍 Поделиться локацией", request_location=True)
    kb.add(button)
    return kb

def language_buttons():
    kb = types.InlineKeyboardMarkup()
    ru_button = types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")
    uz_button = types.InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="lang_uz")
    kb.add(ru_button, uz_button)
    return kb
