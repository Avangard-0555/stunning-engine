import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('delivery_bot.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблиц
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    phone TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cart (
    user_id INTEGER,
    product_name TEXT,
    quantity INTEGER
)
""")
conn.commit()

# Функции для работы с пользователями
def save_user(user_id, name, phone):
    cursor.execute("INSERT INTO users (user_id, name, phone) VALUES (?, ?, ?)", 
                   (user_id, name, phone))
    conn.commit()

# Функции для работы с корзиной
def add_to_cart(user_id, product_name, quantity):
    cursor.execute("INSERT INTO cart (user_id, product_name, quantity) VALUES (?, ?, ?)", 
                   (user_id, product_name, quantity))
    conn.commit()

def remove_from_cart(user_id, product_name):
    cursor.execute("DELETE FROM cart WHERE user_id = ? AND product_name = ?", 
                   (user_id, product_name))
    conn.commit()

def get_cart(user_id):
    cursor.execute("SELECT product_name, quantity FROM cart WHERE user_id = ?", (user_id,))
    return cursor.fetchall()
