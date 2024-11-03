# model_training.py
import tensorflow as tf
from data_processing import prepare_data_for_model, load_data_from_postgres

def build_lstm_model(input_shape):
    """
    Build a multi-layer LSTM model.
    """
    model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(100, return_sequences=True, input_shape=input_shape),
        tf.keras.layers.LSTM(50),
        tf.keras.layers.Dense(25, activation="relu"),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_model(X, y):
    model = build_lstm_model((X.shape[1], 1))
    model.fit(X, y, epochs=10, batch_size=32)
    return model

# Example usage
if __name__ == "__main__":
    raw_data = load_data_from_postgres()
    X, y, scaler = prepare_data_for_model(raw_data)
    model = train_model(X, y)
    model.save("stock_lstm_model.h5")
