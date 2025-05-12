import requests
import yfinance as yf
import time
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
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.live import StockDataStream
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

#Alpaca Config ------------------------------------------------------------------------------------

API_KEY = 'PK9CJ54RHMNWLOZH97BS'
API_SECRET = 'kZEa7PQNWaMeVbrou3cLm0xIFd7KHul5JoeVSdPt'
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(API_KEY, API_SECRET, base_url=BASE_URL)
trading_client = TradingClient(API_KEY, API_SECRET)
account = api.get_account()




def risk_assess(symbol, days): 
    
    ticker = yf.Ticker(f"{symbol}")
    
    history = ticker.history(period=f'{days}d') 
    if history.empty: # check for no history 
        return([0, "insufficient history", "#ffffff"]) # error return

    # 
    
    
    try:
        changes = (history["Close"] - history["Open"]).tolist()
        risk_ratio = abs(min(changes) / max(changes))
        
        if risk_ratio > 1.75:
            risk = "RISKY"
            risk_color = "#fc5c65"

        elif risk_ratio > 1 and risk_ratio < 1.5: 
            risk = "MODERATLEY RISKY"
            risk_color = "#fd9644"
            
        elif risk_ratio == 1: 
            risk = "Not enough data"
            risk_color = "#ffffff"
            
        elif risk_ratio < 1 and risk_ratio > 0.5:
            risk = "MODERATELY SAFE"
            risk_color = "#fed330"
            
        elif risk_ratio < 0.5 and risk_ratio > 0.25: 
            risk = "SAFE"
            risk_color = "#69de26"

        elif risk_ratio < 0.25: 
            risk = "VERY SAFE" 
            risk_color = "#32ff7e"
        
        return([risk_ratio, risk, risk_color])
        
    except:
        return([69, "insufficient or inoperable change data", "#ffffff"])
    
symbol = "AAPL" 
api_token = "4RXPF8Hx1Tlr3nDwJ0GHQxwHStcz9UYybnZYRBfF"
stock_data = requests.get(f"https://api.stockdata.org/v1/data/eod?symbols={symbol}&api_token={api_token}").json()    
print(stock_data)