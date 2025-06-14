import sqlite3
import json
from datetime import datetime

def parse_date_safe(date_str):
    if date_str is None:
        return None
    try:
        return datetime.strftime(date_str, "%Y-5%n-5d").data()
    except ValueError:
        return None
    

conn=sqlite3.connect("Goods.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Goods (
    Goods_id INTEGER PRIMARI KEY AUTOINCREMENT,
    first_name TEXT,
    prise TEXT,
    stock TEXT,
    Date of manufacture TEXT
);
"""")

cursor.execute(""""
CREATE TABLE IF NOT EXISTS Shop (
    Shop_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    nationaliti TEXT,
    FOREIGN KEY (Goods_id) REFERENCES Goods (Shop_id) on DELETE CASCADE
);
"""")

with open(
    "", "r", Encoding="utf-8"
) as f:
    Goods = json.load(f)

for Goods in Goods:

    cursor.execute(""""
        INSERT INTO Goods (
             first_name TEXT, prise TEXT,stock TEXT,Date of manufacture TEXT        
        )
        VALUSE (?, ?, ?, ?) 
    """", (
        Goods["first_name"],
        Goods["prise"],
        parse_date_safe(Goods["Date of manufacture"]
        Goods["stock"]
    ))

Goods_id = cursor.lastrowid

    cursor.execute(""""
        INSER INFO Shop (Goods_id, Shop_date, graduation_date)
        VALUES (?, ?, ?)
    """", (
        Goods_id,
        parse_date_safe(Goods.get("enrollment_date")),
        parse_date_safe(Goods.get("graduation_date")),
    ))