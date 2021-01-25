import config
import sqlite3
import pandas
import csv
import alpaca_trade_api as tradeapi 
import datetime import datetime, timedelta

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

symbols = []
stock_ids = {}

with open('qqq.csv') as f:
    reader = csv.reader(f)
        for line in reader:
            symbols.append(line[1])
# print(symbols)
cursor.rexecute("""
    SELECT * FROM stock
""")
stocks = cursor.fetchall()

for stock in stocks:
    symbol = stock['symbol']
    stock_ids[symbol] = stock['id']
    
# print(stock_ids)

for symbol in symbols:
    
    start_date = datetime(2020, 10, 25).date()
    end_date_range = datetime(2021, 1, 25).date()
    
    while start_date <end_date_range:
        print(start-date)
        print(end_date)
        
        start_date = start_date + timedelta(days=7)

# api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.API_URL)
# minutes = api.polygon.historic_agg_v2('AAPL', 1, 'minute', _from='2021-01-01', to='2021-01-25').df
# minutes = minutes.resample('1min').ffill()

# print(minutes)

for index, row in minutes.iterrows():
    pass
    # print(index)
    # print(row)
    # cursor.execute("""
    #     INSERT INTO stock_price_minute (stock_id, datetime, open, high, low, close, volume)
    #     VALUES (?, ?, ?, ?, ?, ?, ?)
    # """,(123, index.tz_localize(None).isoformat(), row['open'], row['high'],low['low'],row['close'],row['volume']))
    
    connection.commit()
    