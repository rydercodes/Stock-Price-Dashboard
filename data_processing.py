# data_processing.py
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def process_batch_data(stock_data):
    """
    Add moving average to stock data for trend analysis.
    """
    stock_data['Moving_Avg'] = stock_data['Close'].rolling(window=5).mean()
    return stock_data

def prepare_data_for_lstm(stock_data, look_back=60):
    """
    Prepare data for LSTM by scaling and creating sequences.
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(stock_data[['Close']])

    # Create sequences of look_back time steps
    X_train, y_train = [], []
    for i in range(look_back, len(scaled_data)):
        X_train.append(scaled_data[i-look_back:i, 0])
        y_train.append(scaled_data[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)
    
    # Reshape for LSTM input
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    return X_train, y_train, scaler

# Test process function (can be removed in production)
if __name__ == "__main__":
    from data_fetching import fetch_batch_stock_data
    data = fetch_batch_stock_data("AAPL", period="1y", interval="1h")
    processed_data = process_batch_data(data)
    X_train, y_train, scaler = prepare_data_for_lstm(processed_data)
    print(X_train.shape, y_train.shape)
