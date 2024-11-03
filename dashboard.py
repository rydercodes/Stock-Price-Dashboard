# dashboard.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Database connection
engine = create_engine("postgresql://jaber:13711992@localhost:5432/stock_data")

# Function to load transformed data
def load_transformed_data(ticker_symbol):
    """
    Load transformed stock data with moving average from PostgreSQL.
    """
    query = f"""
    SELECT datetime, close, moving_avg
    FROM moving_average
    WHERE ticker = '{ticker_symbol}'
    ORDER BY datetime;
    """
    return pd.read_sql(query, engine)

# Streamlit dashboard setup
st.title("Stock Price and Moving Average Dashboard")

# Select a ticker symbol
ticker_symbol = st.selectbox("Choose a ticker symbol:", ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"])

# Load and display the transformed data
transformed_data = load_transformed_data(ticker_symbol)
st.subheader(f"Stock Prices and Moving Average for {ticker_symbol}")
st.line_chart(transformed_data.set_index('datetime')[['close', 'moving_avg']])
