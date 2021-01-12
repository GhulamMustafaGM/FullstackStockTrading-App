import sqlite3, config 
import alpaca_trade_api as tradeapi

connection = sqlite3.connect(config.DB_FILE)

connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT id, symbol, name FROM stock 
""")

rows = cursor.fetchall()

# symbols = [row['symbol'] for row in rows]
# print(symbols)
symbols = []
stock_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

symbols = ['MSFT']

chunk_size = 200
for i in range(0, len(symbols), chunk_size):
    # print(i)
    # print(i+chunk_size)
    symbol_chunk = symbols[i:i+chunk_size]
    # print(symbol_chunk)
    barsets = api.get_barset(symbol_chunk, 'day')

for symbol in barsets:
    print(f"processing symbol {symbol}")

    print(barsets[symbol])
    
    recent_closes = [bar.c for bar in barsets[symbol]]
    print(len(recent_closes))
    
    for bar in barsets[symbol]:
        stock_id = stock_dict[symbol]
        # cursor.execute("""
        #     INSERT INTO stock_price (stock_id, date, open, high, low, close, volume, sma_20, sma_50, sma_14)
        #     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        # """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v,sma_20, sma_50, sma_14))

# barsets = api.get_barset(['AAPL', 'MSFT'], 'day')
# barsets = api.get_barset(['Z'], 'minute')

# print(barsets)

#loop over the keys in the barsets dictionary 

# for symbol in barsets:
#     print(f"processing symbol {symbol}")

    #loop through each bar for the current symbol in the dictionary
    # for bar in barsets[symbol]:
    #     print(bar.t, bar.o, bar.h, bar.l, bar.c, bar.v)

# minute_bars = api.polygon.historic_agg_v2('Z', 1, 'minute', _from='2020-10-02', to='2020-10-22') 

# for bar in minute_bars:
#     print(bar.timestamp, bar.open, bar.high, bar.low, bar.close)

connection.commit()