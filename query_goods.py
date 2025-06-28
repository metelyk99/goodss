import sqlite3

conn = sqlite3.connect("products.db")
cursor = conn.cursor()

def execute_query(query, params=()):
    try:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(f"Помилка при виконанні запиту: {e}")

print("\nімена продуктів в алфавітному порядку ")

execute_query("""
    SELECT product_name
    FROM goods
    ORDER BY product_name ASC
""")

print("\nВсі продукти з середньою ціною (GPA) понад 15грн:")

execute_query("""
    SELECT prise
    FROM goods
    ORDER BY prise ASC
""")

print("\nВсі продукти які є в наявності")

execute_query("""
    SELECT stock
    FROM goods
    ORDER BY stock ASC
""")
