from flask import Flask, render_template, request, jsonify
from parser import parse_order
from billing import place_order
from kitchen import kitchen_bp
app = Flask(__name__)
app.register_blueprint(kitchen_bp)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/order", methods=["POST"])
def order():
    text = request.json.get("text", "")
    items = parse_order(text)
    if not items:
        return jsonify({"reply": "Sorry, I did not find any dish in your order. Please try again."})
    order_id, subtotal, tax, total = place_order(items)
    lines = [f"{qty} {name}" for _, name, _, qty in items]
    reply = (
        f"You ordered {', '.join(lines)}. "
        f"Subtotal {subtotal:.0f} rupees, GST {tax:.0f} rupees, "
        f"total {total:.0f} rupees. Thank you!"
    )
    return jsonify({"reply": reply, "order_id": order_id, "total": total})

if __name__ == "__main__":
    app.run(debug=True)