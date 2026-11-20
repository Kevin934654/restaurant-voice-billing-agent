import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="restaurant_billing",
    )
def get_menu():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT item_id, name, price FROM menu_items WHERE available = TRUE")
    rows = cur.fetchall()
    conn.close()
    return rows

def create_order(table_number=1):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO orders (table_number) VALUES (%s)", (table_number,))
    conn.commit()
    order_id = cur.lastrowid
    conn.close()
    return order_id

def add_order_item(order_id, item_id, quantity):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO order_items (order_id, item_id, quantity) VALUES (%s, %s, %s)",
        (order_id, item_id, quantity),
    )
    conn.commit()
    conn.close()

def save_bill(order_id, subtotal, tax, total):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO bills (order_id, subtotal, tax, total) VALUES (%s, %s, %s, %s)",
        (order_id, subtotal, tax, total),
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    for item in get_menu():
        print(item["item_id"], item["name"], item["price"])