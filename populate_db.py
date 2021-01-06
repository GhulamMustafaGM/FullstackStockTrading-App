import sqlite3
import alpaca_trade_api as tradeapi

connection = sqlite3.connect('app.db')

cursor = connection.cursor()

api = tradeapi.REST('PK89LCST819PTZPYO116', 'w1j56sCtNqNjzN1ADPqis7PLGwR7Z1ZSEC8KFD97', base_url='https://paper-api.alpaca.markets') # or use ENV Vars shown below
assets = api.list_assets()

for asset in assets:
    # if asset.symbol == 'VXX':
    #     print(asset)
    
    try:
        if asset.status == 'active' and asset.tradable:
            cursor.execute("INSERT INTO stock (symbol, company) VALUES (?, ?)", (asset.symbol, asset.name))
    except Exception as e:
        print(asset.symbol)
        print(e)

connection.commit()