import config
import sqlite3
import pandas
import csv
import alpaca_trade_api as tradeapi 
import datetime import datetime, timedelta

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.API_URL)
minutes = api.polygon.historic_agg_v2('AAPL', 1, 'minute', _from='2021-01-01', to='2021-01-25').df

print(minutes)