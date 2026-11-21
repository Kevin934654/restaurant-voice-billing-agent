import re
from db import get_connection

NUMBER_WORDS = {
    "a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "एक": 1, "दो": 2, "तीन": 3, "चार": 4, "पांच": 5, "पाँच": 5,
    "छह": 6, "छः": 6, "सात": 7, "आठ": 8, "नौ": 9, "दस": 10,
    "ఒకటి": 1, "ఒక": 1, "రెండు": 2, "మూడు": 3, "నాలుగు": 4, "ఐదు": 5,
    "ఆరు": 6, "ఏడు": 7, "ఎనిమిది": 8, "తొమ్మిది": 9, "పది": 10,
    "ek": 1, "do": 2, "teen": 3, "char": 4, "paanch": 5,
    "okati": 1, "rendu": 2, "moodu": 3, "naalugu": 4, "aidu": 5,
}

def load_names():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT item_id, name, price FROM menu_items WHERE available = TRUE")
    items = {r["item_id"]: r for r in cur.fetchall()}
    cur.execute("SELECT item_id, alias FROM menu_aliases")
    aliases = cur.fetchall()
    conn.close()
    names = [(i["name"].lower(), i) for i in items.values()]
    for a in aliases:
        if a["item_id"] in items:
            names.append((a["alias"].lower(), items[a["item_id"]]))
    return names

def parse_order(text):
    text = text.lower()
    found = {}
    # longer names first, so "plain dosa" is matched before a shorter name
    for name, item in sorted(load_names(), key=lambda n: len(n[0]), reverse=True):
        if name in text:
            qty = 1
            match = re.search(r"(\S+)\s+" + re.escape(name), text)
            if match:
                word = match.group(1)
                if word.isdigit():
                    qty = int(word)
                elif word in NUMBER_WORDS:
                    qty = NUMBER_WORDS[word]
            text = text.replace(name, " ", 1)
            if item["item_id"] in found:
                found[item["item_id"]][3] += qty
            else:
                found[item["item_id"]] = [item["item_id"], item["name"], float(item["price"]), qty]
    return [tuple(v) for v in found.values()]

if __name__ == "__main__":
    for item_id, name, price, qty in parse_order("दो मसाला डोसा और एक चाय"):
        print(qty, "x", name, "=", qty * price)