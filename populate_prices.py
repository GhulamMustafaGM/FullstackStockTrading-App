import config 
import alpaca_trade_api as tradeapi

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

barsets = api.get_barset(['AAPL', 'MSFT'], 'day')
print(barsets)
