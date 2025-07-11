import sqlite3
import json
from datetime import datetime

# Функція для безпечного парсингу дати
# Виправлено: використано datetime.strptime для парсингу рядка в дату
# Виправлено: повертає об'єкт date
def parse_date_safe(date_str):
    if date_str is None:
        return None
    try:
        # Формат "%Y-%m-%d" відповідає датам у JSON файлі
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        # Якщо парсинг не вдався, повертаємо None
        print(f"Помилка парсингу дати: '{date_str}'")
        return None

# Підключення до бази даних (або створення, якщо її немає)
conn = sqlite3.connect("products.db")
cursor = conn.cursor()

# Увімкнення підтримки зовнішніх ключів
cursor.execute("PRAGMA foreign_keys = ON;")

# Створення таблиці goods
# Виправлено: 'PRIMARI KEY' на 'PRIMARY KEY'
# Виправлено: прибрано зайві 'TEXT' після назв стовпців у CREATE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS goods (
    goods_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    prise REAL,
    stock INTEGER,
    delivery_day DATE,
    date_manufacture DATE
);
""")

# Створення таблиці Shop
# Виправлено: прибрано зайві 'TEXT' після назв стовпців у CREATE TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS Shop (
    shop_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT,
    product_id INTEGER,
    FOREIGN KEY (product_id) REFERENCES goods (goods_id) ON DELETE CASCADE
);
""")

# Відкриття JSON файлу з даними
# Переконайтеся, що файл 'products.json' знаходиться в тому ж каталозі,
# що й цей скрипт, або вкажіть повний шлях.
try:
    with open("products.json", "r", encoding="utf-8") as f:
        goods_data = json.load(f)
except FileNotFoundError:
    print("Помилка: Файл 'products.json' не знайдено. Переконайтесь, що він існує.")
    conn.close()
    exit()
except json.JSONDecodeError:
    print("Помилка: Неправильний формат JSON у файлі 'products.json'.")
    conn.close()
    exit()


# Вставка даних у таблиці
for good in goods_data:
    try:
        cursor.execute("""
            INSERT INTO goods (
                product_name, prise, stock, delivery_day, date_manufacture
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            good.get("product_name"), # Використовуємо .get() для безпечного доступу
            good.get("prise"),
            good.get("stock"),
            parse_date_safe(good.get("delivery_day")),
            # Зверніть увагу на відповідність назви ключа у JSON ("Date_manufacture" або "date_manufacture")
            # Я використав "date_manufacture" у своєму JSON, але якщо у вас "Date_manufacture", виправте тут
            parse_date_safe(good.get("date_manufacture"))
        ))

        goods_id = cursor.lastrowid # Отримуємо ID щойно вставленого товару

        cursor.execute("""
            INSERT INTO Shop (department, product_id)
            VALUES (?, ?)
        """, (
            good.get("department"),
            goods_id
        ))
    except sqlite3.Error as e:
        print(f"Помилка при вставці даних для товару '{good.get('product_name')}': {e}")
        # Можна додати conn.rollback() тут, щоб скасувати транзакцію, якщо потрібна атомарність

# Зафіксувати зміни в базі даних
conn.commit()
print("Дані успішно імпортовано.")

# Закрити з'єднання з базою даних
conn.close()