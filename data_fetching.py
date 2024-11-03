# data_fetching.py
import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection details
engine = create_engine("postgresql://jaber:13711992@localhost:5432/stock_data")

# List of 10 tickers
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "BABA", "INTC"]

def fetch_and_save_data(tickers, period="1y", interval="1h"):
    """
    Fetches data for each ticker and saves it to PostgreSQL.
    
    Parameters:
        tickers (list): A list of stock ticker symbols.
        period (str): The period of time to fetch data for (default is "1y" for 1 year).
        interval (str): The data interval (e.g., "1h" for hourly data).
    """
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        
        # Fetch historical data from Yahoo Finance
        data = yf.Ticker(ticker).history(period=period, interval=interval)
        
        # Rename columns to match PostgreSQL table schema
        data = data.rename(columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
            "Dividends": "dividends",
            "Stock Splits": "stock_splits"
        })
        
        # Add the ticker column
        data['ticker'] = ticker  # Add ticker column
        
        # Reorder columns to match the PostgreSQL table schema, excluding datetime
        data = data[['open', 'high', 'low', 'close', 'volume', 'dividends', 'stock_splits', 'ticker']]
        
        # Save to PostgreSQL in the "raw_stock_data" table
        data.to_sql("raw_stock_data", engine, if_exists="append", index=False)
        
        print(f"Data for {ticker} saved to PostgreSQL.")

# Run the function
if __name__ == "__main__":
    fetch_and_save_data(TICKERS)
