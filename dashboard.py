import streamlit as st
import pandas as pd
from data_processing import fetch_batch_stock_data, process_batch_data, prepare_data_for_lstm, train_lstm_model

# Title and description
st.title("Stock Price Dashboard")
st.write("This dashboard displays stock prices and predictions.")

# Input for stock symbol
ticker_symbol = st.text_input("Enter a stock symbol (e.g., AAPL)", value="AAPL")

# Fetch and display stock data
if ticker_symbol:
    # Fetch data for the last month with 1-hour interval
    stock_data = fetch_batch_stock_data(ticker_symbol, period="1mo", interval="1h")
    
    # Display raw data
    st.subheader(f"Raw Stock Data for {ticker_symbol}")
    st.write(stock_data.tail(10))  # Show the last 10 rows of data
    
    # Process the data (e.g., moving average)
    processed_data = process_batch_data(stock_data)
    
    # Display processed data with moving average
    st.subheader("Stock Data with Moving Average")
    st.line_chart(processed_data[['Close', 'Moving_Avg']])
    
    # Prepare data and train model
    X_train, y_train, scaler = prepare_data_for_lstm(processed_data)
    model = train_lstm_model(X_train, y_train)
    
    # Optionally, make predictions and display them (using dummy data here as example)
    # This is placeholder code, as the prediction code can vary based on implementation
    st.subheader("LSTM Model Predictions")
    st.write("Add prediction results here.")
