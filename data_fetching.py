import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

# PostgreSQL connection details
engine = create_engine("postgresql://jaber:13711992@db:5432/stock_data")

# List of 10 tickers
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "BABA", "INTC"]

# Check if the table exists and create it if not
def create_table_if_not_exists(engine):
    with engine.connect() as connection:
        try:
            # Use text() to execute raw SQL
            connection.execute(text("SELECT 1 FROM raw_stock_data LIMIT 1;"))
        except ProgrammingError:
            # Table does not exist, so create it
            connection.execute(text("""
                CREATE TABLE raw_stock_data (
                    open DOUBLE PRECISION,
                    high DOUBLE PRECISION,
                    low DOUBLE PRECISION,
                    close DOUBLE PRECISION,
                    volume BIGINT,
                    dividends DOUBLE PRECISION,
                    stock_splits DOUBLE PRECISION,
                    ticker VARCHAR(10)
                );
            """))
            print("Created table raw_stock_data")

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
    create_table_if_not_exists(engine)
    fetch_and_save_data(TICKERS)
