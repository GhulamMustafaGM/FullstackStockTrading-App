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
            start_date = start_date + timedelta(days=4)
            
    print(f"=== Fetching minute bars {start_date}-{end_date} for {symbol}")
    api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.API_URL)
    
    minutes = api.polygon.historic_agg_v2(symbol, 1, 'minute', _from='start_date', to='end_date').df
    minutes = minutes.resample('1min').ffill()

for index, row in minutes.iterrows():
    cursor.execute("""
        INSERT INTO stock_price_minute (stock_id, datetime, open, high, low, close, volume)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,(stock_ids[symbol], index.tz_localize(None).isoformat(), row['open'], row['high'],low['low'],row['close'],row['volume']))

    start_date = start_date + timedelta(days=7)
        
connection.commit()
    