# data_fetching.py
import yfinance as yf
import pandas as pd

def fetch_batch_stock_data(ticker_symbol, period="3mo", interval="1h"):
    """
    Fetch batch stock data for the given period and interval.
    """
    ticker = yf.Ticker(ticker_symbol)
    stock_data = ticker.history(period=period, interval=interval)
    return stock_data

# Test fetch function (can be removed in production)
if __name__ == "__main__":
    data = fetch_batch_stock_data("AAPL", period="3mo", interval="1h")
    print(data.head())
