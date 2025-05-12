###rebalance function 
import requests
import yfinance as yf
from datetime import datetime, timedelta
import pytz
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


while True:
    portfolio = trading_client.get_all_positions()
    for position in portfolio:
        
        if float(position.unrealized_intraday_pl) < 0 and float(position.qty)*0.500 > 0.25: 
            
            market_order_data = MarketOrderRequest(
                    symbol=position.symbol,
                    qty=float(position.qty)*0.500,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.DAY
                    )
            
            market_order = trading_client.submit_order(
                order_data=market_order_data
               )
            
            print(f"sold {position.symbol}")
        
        elif float(position.unrealized_intraday_pl) > 0 and float(position.qty)*float(position.current_price)*0.500 < float(trader.buying_power): 

            market_order_data = MarketOrderRequest(
                    symbol=position.symbol,
                    qty=float(position.qty)*0.500,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.DAY
                    )
            
            market_order = trading_client.submit_order(
                order_data=market_order_data
               )
        
            
            print(f"bought {position.symbol}")
    time.sleep(1)



#we're gonna need smarter scaling
#also the quantity is adding based on some weird thing idk why 