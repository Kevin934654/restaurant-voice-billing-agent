from flask import Blueprint, render_template, jsonify
from db import get_connection

kitchen_bp = Blueprint("kitchen", __name__)

@kitchen_bp.route("/kitchen")
def kitchen_page():
    return render_template("kitchen.html")

@kitchen_bp.route("/kitchen/orders")
def open_orders():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT o.order_id, o.table_number, o.created_at, m.name, oi.quantity "
        "FROM orders o "
        "JOIN order_items oi ON oi.order_id = o.order_id "
        "JOIN menu_items m ON m.item_id = oi.item_id "
        "WHERE o.status = 'open' "
        "ORDER BY o.order_id, m.name"
    )
    rows = cur.fetchall()
    conn.close()
    orders = {}
    for r in rows:
        o = orders.setdefault(r["order_id"], {
            "order_id": r["order_id"],
            "table_number": r["table_number"],
            "time": r["created_at"].strftime("%H:%M"),
            "items": [],
        })
        o["items"].append({"name": r["name"], "quantity": r["quantity"]})
    return jsonify(list(orders.values()))

@kitchen_bp.route("/kitchen/done/<int:order_id>", methods=["POST"])
def mark_done(order_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status = 'done' WHERE order_id = %s", (order_id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})