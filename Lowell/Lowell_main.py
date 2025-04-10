import requests
import yfinance as yf
import time
import math
import smtplib
import customtkinter as ctk
from PIL import Image, ImageTk 

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
    gainers.configure(text = "Found Top!")
    time.sleep(0.5)
    gainers.configure(text = "Find top")
    
# ---------------------------------------------------------------------------------------- analyze the open-close changes 

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
gif_label = ctk.CTkLabel(button_frame, text="")                                                    #
main_display_text = ctk.CTkLabel(frame2, text = "")    
                                                                                                   #
#--------------------------------------------------------------------------------------------------

#button frame elements --------------------------------------------------------------------------------
button_frame.pack(padx=10, pady=10, side="left", fill="both", expand = True)
gainers.pack(padx=10, pady=10, side = "top")
assess.pack(padx=10, pady=10, side = "top")
quit.pack(padx=10, pady=10, side = "top")
gif_label.pack(padx=20, pady=20, side = "bottom")

# Lowell Gif Stuff lol 
gif_image = Image.open("/Users/rehansha/Desktop/Coding/random-projects-lol/Lowell/pixilart-drawing.gif")
frames = []
try:
    while True:
        gif_image.seek(gif_image.tell() + 1)
        frames.append(ImageTk.PhotoImage(gif_image))
except EOFError:
    pass
def update_gif(frame_index):
    if frame_index < len(frames):
        gif_label.configure(image=frames[frame_index])
        button_frame.after(gif_image.info['duration'], lambda: update_gif(frame_index + 1))
    else:
        button_frame.after(gif_image.info['duration'], lambda: update_gif(0))
        
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
        


update_gif(0)
root.mainloop()



