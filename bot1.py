import telebot
import buttons as bt
import database as db
from geopy import Photon

geolocator = Photon(user_agent="Mozilla/5.0")
bot = telebot.TeleBot(token="7Q")

user_language = {}

@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Выберите язык / Tilni tanlang:", reply_markup=bt.language_buttons())

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def set_language(call):
    user_id = call.from_user.id
    lang = call.data.split("_")[1]
    user_language[user_id] = lang

    if lang == "ru":
        bot.send_message(user_id, "Добро пожаловать! Введите своё имя для регистрации:")
    elif lang == "uz":
        bot.send_message(user_id, "Xush kelibsiz! Ro'yxatdan o'tish uchun ismingizni kiriting:")

    bot.register_next_step_handler(call.message, get_name)

def get_name(message):
    user_id = message.from_user.id
    name = message.text
    lang = user_language.get(user_id, "ru")

    if lang == "ru":
        bot.send_message(user_id, "Теперь поделитесь своим номером:", reply_markup=bt.phone_button())
    elif lang == "uz":
        bot.send_message(user_id, "Endi telefon raqamingizni yuboring:", reply_markup=bt.phone_button())

    bot.register_next_step_handler(message, get_phone_number, name)

def get_phone_number(message, name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        lang = user_language.get(user_id, "ru")

        if lang == "ru":
            bot.send_message(user_id, "Отправьте свою локацию:", reply_markup=bt.location_button())
        elif lang == "uz":
            bot.send_message(user_id, "Joylashuvingizni yuboring:", reply_markup=bt.location_button())

        bot.register_next_step_handler(message, get_location, name, phone_number)
    else:
        bot.send_message(user_id, "Пожалуйста, используйте кнопку для отправки номера.")
        bot.register_next_step_handler(message, get_phone_number, name)

def get_location(message, name, phone_number):
    user_id = message.from_user.id
    if message.location:
        latitude = message.location.latitude
        longitude = message.location.longitude
        address = geolocator.reverse((latitude, longitude)).address
    else:
        address = "Адрес не определён"

    db.save_user(user_id, name, phone_number)  # Сохранение пользователя в БД

    lang = user_language.get(user_id, "ru")
    if lang == "ru":
        bot.send_message(user_id, "Вы успешно зарегистрировались!")
    elif lang == "uz":
        bot.send_message(user_id, "Siz muvaffaqiyatli ro'yxatdan o'tdingiz!")

    bot.send_message(user_id, "Главное меню:")

bot.infinity_polling()
