###rebalance function 
import requests
import yfinance as yf
import time
import math
import smtplib
import customtkinter as ctk
from PIL import Image, ImageTk 
import smtplib
from email.mime.text import MIMEText
import alpaca_trade_api as tradeapi

#Alpaca Config ------------------------------------------------------------------------------------

API_KEY = 'PK9CJ54RHMNWLOZH97BS'
API_SECRET = 'kZEa7PQNWaMeVbrou3cLm0xIFd7KHul5JoeVSdPt'
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(API_KEY, API_SECRET, base_url=BASE_URL)
account = api.get_account()

print(account.equity)

