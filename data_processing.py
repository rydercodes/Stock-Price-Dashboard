# data_processing.py
import yfinance as yf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import tensorflow as tf

def fetch_batch_stock_data(ticker_symbol, period="1mo", interval="1h"):
    ticker = yf.Ticker(ticker_symbol)
    stock_data = ticker.history(period=period, interval=interval)
    return stock_data

def process_batch_data(stock_data):
    stock_data['Moving_Avg'] = stock_data['Close'].rolling(window=5).mean()
    return stock_data

def prepare_data_for_lstm(stock_data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(stock_data[['Close']])
    X_train, y_train = [], []
    for i in range(60, len(scaled_data)):
        X_train.append(scaled_data[i-60:i, 0])
        y_train.append(scaled_data[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    return X_train, y_train, scaler

def train_lstm_model(X_train, y_train):
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
        tf.keras.layers.LSTM(50),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=5, batch_size=32)
    return model
