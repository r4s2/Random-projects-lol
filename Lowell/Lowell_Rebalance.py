###rebalance function 
import requests
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import time
import math
import smtplib
import customtkinter as ctk
from PIL import Image, ImageTk 
import smtplib
from email.mime.text import MIMEText
import alpaca_trade_api as tradeapi
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.live import StockDataStream
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

#Alpaca Config ------------------------------------------------------------------------------------

API_KEY = 'PK9CJ54RHMNWLOZH97BS'
API_SECRET = 'kZEa7PQNWaMeVbrou3cLm0xIFd7KHul5JoeVSdPt'
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(API_KEY, API_SECRET, base_url=BASE_URL)
account = api.get_account()
trading_client = TradingClient(API_KEY, API_SECRET)
trader = trading_client.get_account()

def rebalance(symbol, unrealized_intraday_pl, qty, current_price, fractionable):
    unrealized_intraday_pl = float(unrealized_intraday_pl)
    qty = float(qty)
    current_price = float(current_price)
    Buyable = False 
    Sellable = False
    
    if fractionable: 
        order_quantity = float(qty)*0.500
    elif round(float(qty)*0.500) != 0:
        order_quantity = round(float(qty)*0.500)
    else: 
        order_quantity = 0
        Sellable = False
        Buyable = False
        return 0
        
    if qty*current_price*0.500 <= float(trader.buying_power):
        Buyable = True 

    if float(qty)*0.500 > 0.25 and fractionable == True: 
        Sellable = True
    elif round(float(qty)*0.500)> 0 and fractionable == False: 
        Sellable = True 
    
    if Sellable and unrealized_intraday_pl < 0: 
        market_order_data = MarketOrderRequest(
                        symbol=symbol,
                        qty=order_quantity,
                        side=OrderSide.SELL,
                        time_in_force=TimeInForce.DAY
                        )
        try:
            trading_client.submit_order(order_data=market_order_data)
            print(f"Sold {symbol}")
        except: 
            return(0)

    if Buyable and unrealized_intraday_pl > 0: 
        market_order_data = MarketOrderRequest(
                        symbol=symbol,
                        qty=order_quantity,
                        side=OrderSide.BUY,
                        time_in_force=TimeInForce.DAY
                        )
        try:
            trading_client.submit_order(order_data=market_order_data)
            print(f"Bought {symbol}")
        except: 
            return(0)
                
    

# while True:
#     portfolio = trading_client.get_all_positions()
#     for position in portfolio:
        
#         if rebalance(position.symbol, position.unrealized_intraday_pl, position.qty, position.current_price, True) == 0:
#             rebalance(position.symbol, position.unrealized_intraday_pl, position.qty, position.current_price, False)
            
            
        
#         time.sleep(1)



#we're gonna need smarter scaling
#also the quantity is adding based on some weird thing idk why 