from polygon import RESTClient
import requests 

# Initialize the client with your API key
client = RESTClient("9vGon1us_PuekLHSnYXJ5H3BGblgZP1d")

# Define the parameters
ticker = "AAPL"  # The stock ticker symbol
multiplier = 1   # The size of the time window
timespan = "day" # The size of the time window (minute, hour, day, week, month, quarter, year)
from_date = "2025-01-26"  # Start date in YYYY-MM-DD format
to_date = "2025-01-27"    # End date in YYYY-MM-DD format

# Fetch the aggregated data
try:
    response = client.get_aggs(
        ticker=ticker,
        multiplier=multiplier,
        timespan=timespan,
        from_=from_date,
        to=to_date
    )
    # Iterate through the results and print data for each entry
    for result in response:
        print(f"Timestamp (ms): {result.timestamp}, Open: {result.open}, High: {result.high}, "
              f"Low: {result.low}, Close: {result.close}, Volume: {result.volume}")
except Exception as e:
    print(f"An error occurred: {e}")


# - - - - - - - - - - - - - - - - - - - - - - - 

def get_company_news(ticker, api_key, limit=5):

    url = f"https://api.polygon.io/v2/reference/news?ticker={ticker}&limit={limit}&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()

        for article in news_data.get("results", []):
            print(f"Title: {article.get('title', 'No title available')}")
            print(f"Source: {article.get('source', 'Unknown source')}")
            print(f"Summary: {article.get('summary', 'No summary available.')}\n")
            print("-" * 80)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage: Replace YOUR_API_KEY with your actual Polygon.io API key


get_company_news("AAPL", "9vGon1us_PuekLHSnYXJ5H3BGblgZP1d", limit=3)
