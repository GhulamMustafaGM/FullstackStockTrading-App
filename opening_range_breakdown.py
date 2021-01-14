import sqlite3, config 
import alpaca_trade_api as tradeapi
import smtplib, ssl
from datetime import date
from timezone import is_dst

context = ssl.create_default_context()

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute(""" 
    select id from strategy where name = 'opening_range_breakdown'
""")

strategy_id = cursor.fetchone()['id']

cursor.execute("""
    select symbol, name
    from stock
    join stock_strategy on stock_strategy.stock_id = stock.id
    where stock_strategy.strategy_id = ?
""", (strategy_id, ))

stocks = cursor.fetchall()
symbols = [stock['symbol'] for stock in stocks]

# current_date = '2021-01-11'
# current_date = date.today().isoformat()
if is_dst():
    start_minute_bar = f"{current_date} 09:00:00-05:00"
    end_minute_bar = f"{current_date} 09:00:00-05:00"
else:
    start_minute_bar = f"{current_date} 09:00:00-05:00"
    end_minute_bar = f"{current_date} 09:30:00-05:00"

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

orders = api.list_orders()
existing_order_symbols = [order.symbol for order in orders]

messages = []

for symbol in symbols:
    minute_bars = api.polygon.historic_agg_v2(symbol, 1, 'minute', _from=current_date, to=current_date).df

    # print(symbol)
    opening_range_mask = (minute_bars.index >= start_minute_bar) & (minute_bars.index < end_minute_bar)
    opening_range_bars = minute_bars.loc[opening_range_mask]
    # print(opening_range_bars)
    
    opening_range_low = opening_range_bars['low'].min()
    opening_range_high = opening_range_bars['high'].max()
    opening_range = opening_range_high - opening_range_low
    
    # print(opening_range_low)
    # print(opening_range_high)
    # print(opening_range)
    
    after_opening_range_mask = minute_bars.index >= end_minute_bar
    after_opening_range_bars = minute_bars.loc[after_opening_range_mask]
    
    # print(after_opening_range_bars)
    
    after_opening_range_breakdown = after_opening_range_bars[after_opening_range_bars['close'] < opening_range_ligh]
    
    if not after_opening_range_breakdown.empty:
        if symbol not in existing_order_symbols:
        print(after_opening_range_breakdown)
        limit_price = after_opening_range_breakdown.iloc[0]['close']
        # print(limit_price)
        
        message = f"selling short for {symbol} at {limit_price}, closed_below{opening_range_low}\n\n{after_opening_range_breakdown.iloc[0]}\n\n"
        messages.append(message)
        print(message)
        
        api.submit_order(
            symbol='sell',
            side='buy',
            type='market',
            qty='100',
            time_in_force='day',
            order_class='bracket',
            limit_price=limit_price,
            take_profit=dict(
            limit_price=limit_price - opening_range,
            ),
            stop_loss=dict(
            stop_price=limit_price + opening_range,
            )
        )
    else:
        print("Already an order for {symbol}, skipping")
        
        print(messages)
        
        with smtplib.SMTP_SSL(config.EMAIL_HOST, config.EMAIL_PORT, context=context) as server:
            server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
            
            email_message = f"Subject: Trade Notifications for {current_date}\n\n"
            email_message += "\n\n".join(messages)
            
            server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_ADDRESS, email_message)
            server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_SMS, email_message)
            
            