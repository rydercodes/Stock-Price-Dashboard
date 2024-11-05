# dashboard.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Database connection
engine = create_engine("postgresql://jaber:13711992@db:5432/stock_data")

# Function to load transformed data
def load_transformed_data(ticker_symbol):
    """
    Load transformed stock data with moving average from PostgreSQL.
    """
    query = f"""
    SELECT ticker, close,
        AVG(close) OVER (PARTITION BY ticker ORDER BY close ROWS BETWEEN 9 PRECEDING AND CURRENT ROW) AS moving_avg
    FROM raw_stock_data
    WHERE ticker = '{ticker_symbol}'
    ORDER BY close;
    """
    return pd.read_sql(query, engine)

# Streamlit dashboard setup
st.title("Stock Price and Moving Average Dashboard")

# Select a ticker symbol
ticker_symbol = st.selectbox("Choose a ticker symbol:", ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"])

# Load and display the transformed data
transformed_data = load_transformed_data(ticker_symbol)
st.subheader(f"Stock Prices and Moving Average for {ticker_symbol}")

# Ensure columns are numeric
transformed_data['close'] = pd.to_numeric(transformed_data['close'], errors='coerce')
transformed_data['moving_avg'] = pd.to_numeric(transformed_data['moving_avg'], errors='coerce')

# Drop any rows with missing data in 'close' or 'moving_avg'
transformed_data = transformed_data.dropna(subset=['close', 'moving_avg'])

# Plot the line chart with only numeric columns
st.line_chart(transformed_data[['close', 'moving_avg']])
