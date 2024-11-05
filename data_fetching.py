import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine, text, inspect

# PostgreSQL connection details
engine = create_engine("postgresql://jaber:13711992@db:5432/stock_data")

# List of 10 tickers
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "BABA", "INTC"]

def create_table_if_not_exists(engine):
    inspector = inspect(engine)
    if 'raw_stock_data' not in inspector.get_table_names():
        with engine.connect() as connection:
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
    else:
        print("Table raw_stock_data already exists")

def fetch_and_save_data(tickers, period="1y", interval="1h"):
    """
    Fetches data for each ticker and saves it to PostgreSQL.
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
        data['ticker'] = ticker
        # Reorder columns
        data = data[['open', 'high', 'low', 'close', 'volume', 'dividends', 'stock_splits', 'ticker']]
        # Save to PostgreSQL
        data.to_sql("raw_stock_data", engine, if_exists="append", index=False)
        print(f"Data for {ticker} saved to PostgreSQL.")

if __name__ == "__main__":
    print("Starting data_fetching.py")
    create_table_if_not_exists(engine)
    fetch_and_save_data(TICKERS)
    print("Finished data_fetching.py")
