# Install the Alpaca API if you haven't
# pip install alpaca-trade-api

import alpaca_trade_api as tradeapi

# 🔥 Replace these with your real credentials!
API_KEY = 'PK9CJ54RHMNWLOZH97BS'
API_SECRET = 'kZEa7PQNWaMeVbrou3cLm0xIFd7KHul5JoeVSdPt'
BASE_URL = 'https://paper-api.alpaca.markets'  # Use paper trading URL

# Initialize the API
api = tradeapi.REST(API_KEY, API_SECRET, base_url=BASE_URL)

# 1. Check your current account
account = api.get_account()
print(f"Account Status: {account.status}")

# 2. Submit a market order (Buy 1 share of AAPL)
# order = api.submit_order(
#     symbol='AAPL',    
#     qty=1,            
#     side='sell',      
#     type='market',   
#     time_in_force='gtc'  
# )


api._request(
    'POST',
    '/v2/account/portfolio/history',
    {'cash': '500000'}
)


# 3. (Optional) View open positions
positions = api.list_positions()
for position in positions:
    print(f"Holding {position.qty} shares of {position.symbol}")
