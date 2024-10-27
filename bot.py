import telebot
import buttons as bt
import database as db
from geopy import Photon

# Инициализация бота и геолокатора
geolocator = Photon(user_agent="Mozilla/5.0")
bot = telebot.TeleBot(token="7Q")

# Команда /start
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Добро пожаловать в бот доставки!")
    bot.send_message(user_id, "Введите своё имя для регистрации")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_id = message.from_user.id
    name = message.text
    bot.send_message(user_id, "Поделитесь своим номером", reply_markup=bt.phone_button())
    bot.register_next_step_handler(message, get_phone_number, name)

def get_phone_number(message, name):
    user_id = message.from_user.id
    if message.contact:
        phone_number = message.contact.phone_number
        db.save_user(user_id, name, phone_number)  # Сохранение пользователя в БД
        bot.send_message(user_id, "Ваши данные сохранены!")
        bot.send_message(user_id, "Главное меню:")
    else:
        bot.send_message(user_id, "Пожалуйста, используйте кнопку для отправки номера")
        bot.register_next_step_handler(message, get_phone_number, name)

@bot.message_handler(commands=["add_to_cart"])
def add_to_cart(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введите название товара:")
    bot.register_next_step_handler(message, get_product_name)

def get_product_name(message):
    user_id = message.from_user.id
    product_name = message.text
    bot.send_message(user_id, f"Введите количество для {product_name}:")
    bot.register_next_step_handler(message, get_product_quantity, product_name)

def get_product_quantity(message, product_name):
    user_id = message.from_user.id
    try:
        quantity = int(message.text)
        db.add_to_cart(user_id, product_name, quantity)
        bot.send_message(user_id, f"{product_name} добавлен(о) в корзину!")
    except ValueError:
        bot.send_message(user_id, "Количество должно быть числом. Попробуйте снова.")
        bot.register_next_step_handler(message, get_product_quantity, product_name)

@bot.message_handler(commands=["view_cart"])
def view_cart(message):
    user_id = message.from_user.id
    cart = db.get_cart(user_id)
    if cart:
        cart_content = "\n".join([f"{item[0]}: {item[1]} шт." for item in cart])
        bot.send_message(user_id, f"Ваша корзина:\n{cart_content}")
    else:
        bot.send_message(user_id, "Ваша корзина пуста.")

@bot.message_handler(commands=["remove_from_cart"])
def remove_from_cart(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введите название товара для удаления:")
    bot.register_next_step_handler(message, confirm_remove_from_cart)

def confirm_remove_from_cart(message):
    user_id = message.from_user.id
    product_name = message.text
    db.remove_from_cart(user_id, product_name)
    bot.send_message(user_id, f"{product_name} удалён из корзины.")

# Запуск бота
bot.infinity_polling()
