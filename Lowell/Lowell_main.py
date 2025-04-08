import requests
import yfinance as yf
import time
import math
import smtplib
import customtkinter as ctk

# ---------------------------------------------------------------------------------------- send messages 

def send_sms_via_email(to_number, carrier_gateway, from_email, from_password, message):

    server = smtplib.SMTP('smtp.gmail.com', 587)  
    server.starttls()
    server.login(from_email, from_password)


    to_email = f"{to_number}@{carrier_gateway}"
    server.sendmail(from_email, to_email, message)
    server.quit()
    print("Message sent successfully!")

from_email = 'rehan.sha0070@gmail.com' 
from_password = 'sesx ovio jaol lcxv' 
to_number = '2069100070' 
carrier_gateway = 'txt.att.net'  
message = "Hello, this is a test SMS sent from Python!"

# ---------------------------------------------------------------------------------------- find the top gainers

api_key = "27O7Q6OP7I6N4YHE"
reqlink = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={api_key}"
avrequest = requests.get(reqlink)
#todays_top = []
todays_top = ['AMPGW', 'PWUPW', 'JSPRW', 'WHLRL', 'MNYWW', 'NUVB+']

def top_gainers():
    for stock in avrequest.json()['top_gainers']:
        todays_top.append(stock['ticker'])
        main_display_text.configure(text = str(stock['ticker']))
    print("found top gainers")
    
# ---------------------------------------------------------------------------------------- analyze the open-close changes 

#assessing risk      FIX MODERATE RISK, the 1.0 value iS NOT WORKING WELL 
def risk_assess(symbol, days):
    
    ticker = yf.Ticker(f"{symbol}")
    
    history = ticker.history(period=f'{days}d') 
    if history.empty: # check for no history 
        print(f"DEBUG: {symbol} has no history data")
        return([0, "nothing provided", "#ffffff"]) # error return
        
    changes = (history["Close"] - history["Open"]).tolist()
    if not changes: # check for price change data 
        print(f"DEBUG: {symbol} has no price change data")
        return([0, "nothing provided", "#ffffff"])

    try:
        least = min(changes)
        greatest = max(changes)
        
        if greatest == 0.0:
            print(f"DEBUG: {symbol} has no movement")
            return([0, "nothing provided", "#ffffff"])
        
        risk_ratio = abs(least / greatest)

    except Exception as e:
        print(f"DEBUG: Error for {symbol} -> {str(e)}")
        return([0, "nothing provided", "#ffffff"])
    
        
    if risk_ratio > 1.75:
        risk = "VERY RISKY"
        risk_color = "#e74c3c"

    elif risk_ratio > 1 and risk_ratio < 1.5: 
        risk = "RISKY"
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
        
    else:
        return(["error in information, unable to create profile", 6.9, "#ffffff"])
        
    return([risk_ratio, risk, risk_color])

def create_total_assessment():

    
    # Clear previous buttons if necessary
    for widget in frame2.winfo_children():
        widget.destroy()
    
    # Loop over the top gainers and assess risk
    for stock in todays_top:

        # Create a new object and button for the stock
        AnalyzedStock( stock, [risk_assess(stock, 7)[2], risk_assess(stock, 1)[2]], [risk_assess(stock, 7)[0], risk_assess(stock, 1)[0]], [risk_assess(stock, 7)[1], risk_assess(stock, 1)[1]] )
    
    assess.configure(text="Create Assessment", command=create_total_assessment)
    
    #send_sms_via_email(to_number, carrier_gateway, from_email, from_password, message)    

# ---------------------------------------------------------------------------------------- create interface 

root = ctk.CTk() 
root.geometry("800x400")
root.title("Lowell")
root.resizable(False, False)

#all instances ------------------------------------------------------------------------------------
#   frames                                                                                         #
button_frame = ctk.CTkFrame(root)                                                                  #
frame2 = ctk.CTkScrollableFrame(root)                                                              #
                                                                                                   #
#   elements                                                                                       #
gainers = ctk.CTkButton(button_frame, text = "Find top", command=top_gainers)                      #
assess = ctk.CTkButton(button_frame, text = "Create Assessment", command=create_total_assessment)  #
quit = ctk.CTkButton(button_frame, text = 'End Lowell', command=exit)                              #
main_display_text = ctk.CTkLabel(frame2, text = '')                                                #
#--------------------------------------------------------------------------------------------------

#button frame elements --------------------------------------------------------------------------------
button_frame.pack(padx=10, pady=10, side="left", fill="both", expand = True)
gainers.pack(padx=10, pady=10, side = "top")
assess.pack(padx=10, pady=10, side = "top")
quit.pack(padx=10, pady=10, side = "top")

#scroll frame elements --------------------------------------------------------------------------------
frame2.pack(padx=10, pady=10, side="right", fill="both", expand = True)



#stock template
class AnalyzedStock():
    def __init__ (self, stock_name, risk_color,  risk_ratio, risk_ID):
        self.risk_color = risk_color
        self.stock_name = stock_name
        self.risk_ratio = risk_ratio
        self.risk_ID = risk_ID
        self.stock_button = ctk.CTkButton(frame2, text = self.stock_name, fg_color = self.risk_color[0], command = self.sentiments_and_analysis)
        self.stock_button.pack(pady = 10, side = "top")
                
    def kill(self): #probably need to find something better here
        exit()

    def sentiments_and_analysis(self):
        #constants for tkinter
        font_tuple = ("Arial", 20)
        
        #set up GUI 
        top_window = ctk.CTkToplevel(root)
        top_window.geometry("900x400")  
        top_window.title(self.stock_name)
        
        news_frame = ctk.CTkFrame(top_window)
        stock_info_frame = ctk.CTkFrame(news_frame)
        da_news = ctk.CTkLabel(news_frame, text = '', justify = 'left')
        ratio_label_LT = ctk.CTkLabel(stock_info_frame, text = f"Long Term Asessment: \n {self.risk_ratio[0]}, {self.risk_ID[0]}", font = font_tuple) #Long term info
        ratio_label_ST = ctk.CTkLabel(stock_info_frame, text = f"Short Term Asessment: \n {self.risk_ratio[1]}, {self.risk_ID[1]}", font = font_tuple) #Short term info
        button = ctk.CTkButton(top_window, text="Close", command=top_window.destroy)
        
        # packing
        stock_info_frame.pack(padx=10, pady=10, side = "top" ) 
        news_frame.pack(padx=10, pady=10, side = "top" )
        button.pack(pady=10, side = "bottom")
        da_news.pack(padx=10, pady=10, side = 'top')
        ratio_label_LT.pack(padx=10, pady=10, side = 'top')
        #ratio_label_ST.pack(padx=10, pady=10, side = 'top')         TURNING OFF SHORT TERM FOR NOW BC IT JUST DON WORK

        
        #news function
        news = yf.Ticker(self.stock_name).news
        displayed_news = ''
        
        for article in range(0,4): 
            displayed_news += str(news[article]["content"]["title"])
            displayed_news += "\n"
        
        if displayed_news == '':
            displayed_news = "No News or Sentiment Available"
            
        da_news.configure(text=displayed_news)
        



root.mainloop()



