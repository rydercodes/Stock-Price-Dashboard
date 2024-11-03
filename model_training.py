# model_training.py
import tensorflow as tf
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

def build_lstm_model(input_shape):
    """
    Build a deeper LSTM model with additional layers for complexity.
    """
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(100, return_sequences=True, input_shape=input_shape),
        tf.keras.layers.LSTM(100, return_sequences=True),
        tf.keras.layers.LSTM(50),
        tf.keras.layers.Dense(25, activation="relu"),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_lstm_model(model, X_train, y_train, epochs=10, batch_size=32):
    """
    Train the LSTM model on the data.
    """
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)
    return model

def evaluate_model(model, X_train, y_train):
    predictions = model.predict(X_train)
    mse = mean_squared_error(y_train, predictions)
    mae = mean_absolute_error(y_train, predictions)
    return mse, mae

# Test training function (can be removed in production)
if __name__ == "__main__":
    from data_processing import prepare_data_for_lstm, process_batch_data
    from data_fetching import fetch_batch_stock_data

    data = fetch_batch_stock_data("AAPL", period="3mo", interval="1h")
    processed_data = process_batch_data(data)
    X_train, y_train, scaler = prepare_data_for_lstm(processed_data)

    model = build_lstm_model((X_train.shape[1], 1))
    model = train_lstm_model(model, X_train, y_train)
    mse, mae = evaluate_model(model, X_train, y_train)
    print(f"Model MSE: {mse}, Model MAE: {mae}")
