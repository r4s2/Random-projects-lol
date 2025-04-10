import requests
import yfinance as yf
import time
import math
import smtplib
import customtkinter as ctk
from PIL import Image, ImageTk 

todays_top = ['AMPGW', 'PWUPW', 'JSPRW', 'WHLRL', 'MNYWW', 'NUVB+', 'FMTO', 'NLSPW', 'SXTPW', 'NAOV', 'FATN', 'ZVSA', 'MSPRZ', 'CELG^', 'IXHL', 'ABPWW', 'SES+', 'SXTP', 'FAASW', 'AGH', 'VEEE', 'SBFMW', 'JZXN', 'CAPS', 'SPPL', 'REVB']


def risk_assess(symbol, days):
    
    ticker = yf.Ticker(f"{symbol}")
    
    history = ticker.history(period=f'{days}d') 
    if history.empty: # check for no history 
        return([0, "insufficient history", "#ffffff"]) # error return

    try:
        changes = (history["Close"] - history["Open"]).tolist()
        risk_ratio = abs(min(changes) / max(changes))
        
        if risk_ratio > 1.75:
            risk = "RISKY"
            risk_color = "#e74c3c"

        elif risk_ratio > 1 and risk_ratio < 1.5: 
            risk = "MODERATLEY RISKY"
            risk_color = "#f39c12"
            
        elif risk_ratio == 1: 
            risk = "Not enough data"
            risk_color = "#ffffff"
            
        elif risk_ratio < 1 and risk_ratio > 0.5:
            risk = "MODERATELY SAFE"
            risk_color = "#a1eb17"
            
        elif risk_ratio < 0.5 and risk_ratio > 0.25: 
            risk = "SAFE"
            risk_color = "#44bd32"

        elif risk_ratio < 0.25: 
            risk = "VERY SAFE" 
            risk_color = "#7bed9f"
        
        return([risk_ratio, risk, risk_color])
        
    except:
        return([69, "insufficient or inoperable change data", "#ffffff"])
