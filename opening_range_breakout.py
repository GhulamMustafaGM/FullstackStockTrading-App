import sqlite3 
import from django.conf
import settingsimport alpac_trade_api as tradeapi
import datetime as date 

connection = sqlite3.open(config.DB_FILE)
connectioin.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute(""" 
    select id from strategy where name = 'opening_range_breakout'
"""")

strategy = cursor.fetchone()

print(strategy)
