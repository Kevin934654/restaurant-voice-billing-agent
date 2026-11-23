from flask import Flask, render_template, request, jsonify
from parser import parse_order
from billing import place_order
from kitchen import kitchen_bp
from db import get_connection

app = Flask(__name__)
app.register_blueprint(kitchen_bp)

TEXT = {
    "en": {
        "none": "Sorry, I did not find any dish in your order. Please try again.",
        "bill": "You ordered {items}. Subtotal {s} rupees, GST {t} rupees, total {tot} rupees. Thank you!",
    },
    "hi": {
        "none": "माफ़ कीजिए, मुझे ऑर्डर में कोई डिश नहीं मिली। कृपया फिर से बोलिए।",
        "bill": "आपने ऑर्डर किया: {items}। सबटोटल {s} रुपये, जीएसटी {t} रुपये, कुल {tot} रुपये। धन्यवाद!",
    },
    "te": {
        "none": "క్షమించండి, మీ ఆర్డర్‌లో ఏ వంటకం కనిపించలేదు. దయచేసి మళ్లీ చెప్పండి.",
        "bill": "మీరు ఆర్డర్ చేసినవి: {items}. సబ్ టోటల్ {s} రూపాయలు, జీఎస్టీ {t} రూపాయలు, మొత్తం {tot} రూపాయలు. ధన్యవాదాలు!",
    },
}

def menu_by_category():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT name, price, category FROM menu_items "
        "WHERE available = TRUE ORDER BY category, name"
    )
    rows = cur.fetchall()
    conn.close()
    groups = {}
    for r in rows:
        groups.setdefault(r["category"], []).append(r)
    return groups

@app.route("/")
def home():
    return render_template("index.html", menu=menu_by_category())

@app.route("/order", methods=["POST"])
def order():
    text = request.json.get("text", "")
    lang = request.json.get("lang", "en")
    if lang not in TEXT:
        lang = "en"
    items = parse_order(text)
    if not items:
        return jsonify({"reply": TEXT[lang]["none"]})
    order_id, subtotal, tax, total = place_order(items)
    lines = ", ".join(f"{qty} {name}" for _, name, _, qty in items)
    reply = TEXT[lang]["bill"].format(
        items=lines, s=f"{subtotal:.0f}", t=f"{tax:.0f}", tot=f"{total:.0f}"
    )
    return jsonify({"reply": reply, "order_id": order_id, "total": total})

if __name__ == "__main__":
    app.run(debug=True)