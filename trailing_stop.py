import config
import alpaca_trade_api as tradeapi
import helpers import calcualte_quantity

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

symbols = ['SPY', 'IWM', 'dia']

for symbol in symbols:
    api.submit_order()
    
    quote = api.get_last_quote(symbol)
    api.submit_order {
        symbol=symbol,
        side='buy',
        type='market',
        qty=calculate_quantity(quote.bidprice),
        time_in_force='day'
    }
    