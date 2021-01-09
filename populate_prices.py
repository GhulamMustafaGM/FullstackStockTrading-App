import config 
import alpaca_trade_api as tradeapi

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

barsets = api.get_barset(['AAPL', 'MSFT'], 'day')
barsets = api.get_barset(['Z'], 'minute')

print(barsets)

#loop over the keys in the barsets dictionary 

for symbol in barsets:
    print(f"processing symbol {symbol}")

    #loop through each bar for the current symbol in the dictionary
    for bar in barsets[symbol]:
        print(bar.t, bar.o, bar.h, bar.l, bar.c, bar.v)

# minute_bars = api.polygon.historic_agg_v2('Z', 1, 'minute', _from='2020-10-02', to='2020-10-22') 

# for bar in minute_bars:
#     print(bar.timestamp, bar.open, bar.high, bar.low, bar.close)