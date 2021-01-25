import config
import sqlite3
import pandas
import csv
import alpaca_trade_api as tradeapi 
import datetime import datetime, timedelta

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

