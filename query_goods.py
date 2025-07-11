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

# print("\nімена продуктів в алфавітному порядку ")

# execute_query("""
#     SELECT product_name
#     FROM goods
#     ORDER BY product_name ASC
# """)
# print("\nвибираємо всі записи які є в таблиці: ")

# execute_query("""
#     SELECT *
#     FROM goods
# """)

# print("\nВсі продукти з середньою ціною (GPA) понад 15грн:")

# execute_query("""
#     SELECT  product_name, prise
#     FROM goods
#     WHERE prise > 40
#     ORDER BY prise DESC
# """)

# print("\nТоп п'ять продуктів які є на складі більше 50")

# execute_query("""
#     SELECT product_name, prise, stock
#     FROM goods
#     WHERE stock > 50
#     ORDER BY prise DESC
#     LIMIT 5
# """)

# print("\nВсі віділи які є в магазині")

# execute_query("""
#     SELECT DISTINCT department
#     FROM Shop
              
# """)

print("\nНайдешевший продукт молочного віділу")

execute_query("""
    SELECT product_name, department, MIN(prise)
    FROM Shop
    INNER JOIN goods
    ON goods.goods_id = shop.product_id
    WHERE department = "Молочний відділ"
              
""")
