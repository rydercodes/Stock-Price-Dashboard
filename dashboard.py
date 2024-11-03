# dashboard.py
import streamlit as st
from data_fetching import fetch_batch_stock_data
from data_processing import process_batch_data, prepare_data_for_lstm
from model_training import build_lstm_model, train_lstm_model
import numpy as np

# Streamlit UI components
st.title("Enhanced Multi-Ticker Stock Price Dashboard")
st.write("This dashboard shows stock price data, trends, and predictions for multiple stocks.")

# Define a list of 10 stock tickers
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "BABA", "INTC"]

# Loop through each ticker to fetch, process, and display data
for ticker_symbol in tickers:
    st.header(f"Stock Data for {ticker_symbol}")
    
    # Fetch stock data for 1 year with a 1-hour interval
    stock_data = fetch_batch_stock_data(ticker_symbol, period="1y", interval="1h")
    
    # Display raw data table
    st.subheader(f"Raw Data for {ticker_symbol}")
    st.write(stock_data.tail())

    # Process the data (add moving average)
    processed_data = process_batch_data(stock_data)
    
    # Display line chart with closing price and moving average
    st.subheader(f"Closing Price and Moving Average for {ticker_symbol}")
    st.line_chart(processed_data[['Close', 'Moving_Avg']])
    
    # Prepare data for LSTM and train model
    X_train, y_train, scaler = prepare_data_for_lstm(processed_data)
    model = build_lstm_model((X_train.shape[1], 1))
    model = train_lstm_model(model, X_train, y_train)
    
    # Prediction example (predicting the next hour's price)
    last_data = processed_data['Close'][-60:].values.reshape(-1, 1)
    last_data_scaled = scaler.transform(last_data)
    X_pred = np.reshape(last_data_scaled, (1, 60, 1))
    predicted_price = scaler.inverse_transform(model.predict(X_pred))
    
    # Display the predicted next price
    st.subheader(f"Predicted Next Hour Price for {ticker_symbol}")
    st.write(f"Predicted Price: ${predicted_price[0][0]:.2f}")

    # Add a separator between tickers
    st.markdown("---")
