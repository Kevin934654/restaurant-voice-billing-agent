# Restaurant Voice Billing Agent

A voice agent that takes a restaurant order by speech, saves it in MySQL, adds 5% GST and speaks the bill back.

## Tech stack
Python, Flask, MySQL, browser speech recognition and text to speech

## How it works
1. Customer speaks an order, for example "two masala dosa and one filter coffee".
2. The order text is matched against the menu table in MySQL.
3. The order and bill are saved in the database.
4. The total is spoken back to the customer.

## Setup
1. Install MySQL and create the restaurant_billing database with the tables menu_items, orders, order_items and bills.
2. pip install -r requirements.txt
3. Create a .env file with DB_PASSWORD=your_mysql_password
4. Run python app.py and open http://127.0.0.1:5000 in Chrome.