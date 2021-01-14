import sqlite3, config 
import alpaca_trade_api as tradeapi
from datetime import date, datetime
from timezone import is_dst

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute(""" 
    select id from strategy where name = 'opening_range_breakout'
""")

strategy_id = cursor.fetchone()['id']

cursor.execute("""
    select symbol, name
    from stock
    join stock_strategy on stock_strategy.stock_id = stock.id
    where stock_strategy.strategy_id = ?
""", (strategy_id, ))

stocks = cursor.fetchall()
symbols = [stock['symbol'] for stock in stocks]

# current_date = '2021-01-11'
# current_date = date.today().isoformat()
if is_dst():
    start_minute_bar = f"{current_date} 09:00:00-05:00"
    end_minute_bar = f"{current_date} 09:00:00-05:00"
else:
    start_minute_bar = f"{current_date} 09:00:00-05:00"
    end_minute_bar = f"{current_date} 09:30:00-05:00"

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

orders = api.list_orders()
existing_order_symbols = [order.symbol for order in orders]

messages = []

for symbol in symbols:
    minute_bars = api.polygon.historic_agg_v2(symbol, 1, 'minute', _from=current_date, to=current_date).df