import requests
import yfinance as yf
import time
import math
import smtplib
import customtkinter as ctk
from PIL import Image, ImageTk 

ctk.set_default_color_theme("green") 
ctk.set_appearance_mode("dark")
root = ctk.CTk() 
root.geometry("800x700")
root.title("Lowell")
root.resizable(False, False)


#all instances ------------------------------------------------------------------------------------
#   frames                                                                                         
button_frame = ctk.CTkFrame(root)                                                                  
frame2 = ctk.CTkScrollableFrame(root)                                                              
                                                                                                   
#   elements                                                                                       
gainers = ctk.CTkButton(button_frame, text = "Find top", command=None)                      
assess = ctk.CTkButton(button_frame, text = "Create Assessment", command=None)  
to_buy = ctk.CTkScrollableFrame(button_frame, label_text= "Buy List")
purchase = ctk.CTkButton(button_frame, text="Buy")
quit = ctk.CTkButton(button_frame, text = 'End Lowell', command=exit)                              
gif_label = ctk.CTkLabel(button_frame, text="")                                                    
                                                                                                   
#--------------------------------------------------------------------------------------------------

#button frame elements --------------------------------------------------------------------------------
button_frame.pack(padx=10, pady=10, side="left", fill="both", expand = True)
gainers.pack(padx=10, pady=10, side = "top")
assess.pack(padx=10, pady=10, side = "top")
to_buy.pack(padx=10, pady=10, side = "top")
purchase.pack(padx=10, pady=10, side= "top")
quit.pack(padx=10, pady=10, side = "bottom")
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

# ---------------------------------------------------------------------------------------- find the top gainers

api_key = "27O7Q6OP7I6N4YHE"
reqlink = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={api_key}"
avrequest = requests.get(reqlink)
todays_top = []


def top_gainers():
    for stock in avrequest.json()['top_gainers']:
        if "+" in stock['ticker'] or "^" in stock['ticker']:
            todays_top.append(stock['ticker'][:-1:])
        else:
            todays_top.append(stock['ticker'])
        
gainers.configure(command = top_gainers)  
    
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

def create_total_assessment():

    
    # Clear previous buttons if necessary
    for widget in frame2.winfo_children():
        widget.destroy()
    
    # Loop over the top gainers and assess risk
    for stock in todays_top:
        # Create a new object and button for the stock
        AnalyzedStock( stock, risk_assess(stock, 7)[2], risk_assess(stock, 7)[0], risk_assess(stock, 7)[1] )
    
    assess.configure(text="Create Assessment", command=create_total_assessment)
    
    #send_sms_via_email(to_number, carrier_gateway, from_email, from_password, message)    
assess.configure(command = create_total_assessment)

def send_chosen_stocks(): 
    message = ''
    total_price = 0
    to_buy_list = []
    prices = []
    
    for widget in to_buy.winfo_children(): 
        to_buy_list.append(widget.cget("text")[:str(widget.cget("text")).find(" "):])
        prices.append((float(yf.Ticker(str(widget.cget("text"))[:str(widget.cget("text")).find(" "):]).history(period='1d')['Close'][0]) * float(str(widget.cget("text"))[(str(widget.cget("text")).find("*")+1):])))
        total_price += float(yf.Ticker(str(widget.cget("text"))[:str(widget.cget("text")).find(" "):]).history(period='1d')['Close'][0]) * float(str(widget.cget("text"))[(str(widget.cget("text")).find("*")+1):])
        
        message += f"stock: {str(to_buy_list[-1])} \n price: {str(prices[-1])} \n\n"
    message += str(total_price)
     
    preview = ctk.CTkToplevel(root)
    preview.geometry("400x500") 
    preview.title("Final Purchase Preview")
    
    preview_text_frame = ctk.CTkScrollableFrame(preview, width = '300') 
    preview_text = ctk.CTkLabel(master = preview_text_frame, text = message)
    cancel_button = ctk.CTkButton(preview, text = "Cancel", command = preview.destroy)
    send_receipt = ctk.CTkButton(preview, text = "Send to Phone", command = lambda: send_sms_via_email(to_number, carrier_gateway, from_email, from_password, message))
    
      
    preview_text_frame.pack(padx = 10, pady = 10, side = 'top')
    preview_text.pack(padx = 10, pady = 10, side = "top")
    cancel_button.pack(padx = 10, pady = 10)
    send_receipt.pack(padx = 10, pady = 10)
    
    
    
purchase.configure(command = send_chosen_stocks)    

# ---------------------------------------------------------------------------------------- create interface 



#stock template
class AnalyzedStock():
    def __init__ (self, stock_name, risk_color,  risk_ratio, risk_ID):
        self.risk_color = risk_color
        self.stock_name = stock_name
        self.risk_ratio = risk_ratio
        self.risk_ID = risk_ID
        self.price = 0 
        self.stock_button = ctk.CTkButton(frame2, text = self.stock_name, fg_color = self.risk_color, command = self.sentiments_and_analysis, font = ("Arial", 15, "bold", ), text_color = "black")
        self.stock_button.pack(pady = 10, side = "top")

        if self.risk_ratio == 69 or self.risk_ratio == 0 or self.risk_ratio == 1: 
            self.stock_button.destroy()

        
    def sentiments_and_analysis(self):
        #constants for tkinter
        font_tuple = ("Arial", 20)
        
        #set up GUI 
        top_window = ctk.CTkToplevel(root)
        top_window.geometry("950x350")  
        top_window.title(self.stock_name)
        button = ctk.CTkButton(top_window, text="Close", command=top_window.destroy)
        price_frame = ctk.CTkFrame(top_window)
        news_frame = ctk.CTkFrame(top_window)
        
        stock_info_frame = ctk.CTkFrame(news_frame)
        da_news = ctk.CTkLabel(news_frame, text = '', justify = 'left')
        
        ratio_label_LT = ctk.CTkLabel(stock_info_frame, text = f"Long Term Asessment: \n {self.risk_ratio}, {self.risk_ID}", font = font_tuple) #Long term info
        
        price = yf.Ticker(self.stock_name).history(period='1d')['Close'][0]
        price_label = ctk.CTkLabel(price_frame, text = f"{str(price)[:str(price).find('.') + 4]}", font = ("Arial", 65, "bold"))
        purchase_button = ctk.CTkButton(price_frame, text = "Add to List", command = self.move_to_buy_list)
        global purchase_quantity
        purchase_quantity = ctk.CTkEntry(price_frame, placeholder_text = "Qty")
        
        
        # packing
        button.pack(pady=10, side = "bottom")
        
        stock_info_frame.pack(padx=10, pady=10, side = "top") 
        news_frame.pack(padx=10, pady=10, side = "left")
        
        price_frame.pack(padx=10, pady=10, side = "left")
        price_label.pack(padx=10, pady=10, side="top")
        purchase_quantity.pack(padx=10, pady=10, side="left")
        purchase_button.pack(padx=10, pady=10, side = "right")
        
        da_news.pack(padx=10, pady=10, side = 'top')
        ratio_label_LT.pack(padx=10, pady=10, side = 'top')

        

        #news function
        news = yf.Ticker(self.stock_name).news
        displayed_news = ''

        for article in range(0,4): 
            displayed_news += str(news[article]["content"]["title"])
            displayed_news += "\n"
        
        if displayed_news == '':
            displayed_news = "No News or Sentiment Available"
            
        da_news.configure(text=displayed_news)


        
    #it's in the name 
    def move_to_buy_list(self):
        
        to_buy_list = [
            widget.cget("text")[:str(widget.cget("text")).find(" "):]
            for widget in to_buy.winfo_children() 
        ]        
        
        if self.stock_name not in to_buy_list: 
            name = str(self.stock_name) + " *" + str(purchase_quantity.get())
            listed_stock = ctk.CTkButton(to_buy, text = name, fg_color = "#27e4f5", hover_color="#ff7675", command = None, font = ("Arial", 15, "bold"))
            
            def destroy_list_item():
                listed_stock.destroy()  
                
                self.price = 0
                for widget in to_buy.winfo_children(): 
                    string = str(widget.cget("text"))
                    self.price += float(yf.Ticker(string[:string.find(" "):]).history(period='1d')['Close'][0]) * float(string[(string.find("*")+1):])  
                purchase.configure(text= "Purchase at " + str(self.price)[:(str(self.price).find(".")+3)]) 
                           
            listed_stock.configure(command = destroy_list_item)
            listed_stock.pack(padx=10, pady=10, side='top')
            
        for widget in to_buy.winfo_children(): 
            string = str(widget.cget("text"))
            self.price += float(yf.Ticker(string[:string.find(" "):]).history(period='1d')['Close'][0]) * float(string[(string.find("*")+1):])
        
        purchase.configure(text= "Purchase at " + str(self.price)[:(str(self.price).find(".")+3)]) 
                
            
            
update_gif(0)
root.mainloop()



