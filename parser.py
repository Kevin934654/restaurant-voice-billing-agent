import re
from db import get_menu

NUMBER_WORDS = {
    "a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
}

def parse_order(text):
    text = text.lower()
    menu = get_menu()
    found = []
    # check longer dish names first, so "plain dosa" is matched before "dosa"
    for item in sorted(menu, key=lambda m: len(m["name"]), reverse=True):
        name = item["name"].lower()
        if name in text:
            qty = 1
            match = re.search(r"(\d+|[a-z]+)\s+" + re.escape(name), text)
            if match:
                word = match.group(1)
                if word.isdigit():
                    qty = int(word)
                elif word in NUMBER_WORDS:
                    qty = NUMBER_WORDS[word]
            found.append((item["item_id"], item["name"], float(item["price"]), qty))
            text = text.replace(name, " ", 1)
    return found

if __name__ == "__main__":
    for item_id, name, price, qty in parse_order("two masala dosa and one filter coffee"):
        print(qty, "x", name, "=", qty * price)