from db import create_order, add_order_item, save_bill

GST_RATE = 0.05

def calculate_bill(items):
    subtotal = sum(price * qty for _, _, price, qty in items)
    tax = round(subtotal * GST_RATE, 2)
    total = round(subtotal + tax, 2)
    return subtotal, tax, total

def place_order(items, table_number=1):
    order_id = create_order(table_number)
    for item_id, name, price, qty in items:
        add_order_item(order_id, item_id, qty)
    subtotal, tax, total = calculate_bill(items)
    save_bill(order_id, subtotal, tax, total)
    return order_id, subtotal, tax, total

if __name__ == "__main__":
    from parser import parse_order
    items = parse_order("two masala dosa and one filter coffee")
    order_id, subtotal, tax, total = place_order(items)
    print("Order", order_id)
    print("Subtotal:", subtotal)
    print("GST 5%:", tax)
    print("Total:", total)