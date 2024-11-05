# data_processing.py
import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Database connection
engine = create_engine("postgresql://jaber:13711992@db:5432/stock_data")

def load_data_from_postgres():
    """
    Load data from PostgreSQL.
    """
    query = "SELECT * FROM raw_stock_data"
    return pd.read_sql(query, engine)

def prepare_data_for_model(data, look_back=60):
    """
    Scales and prepares data for the LSTM model.
    """
    data = data[['close', 'ticker']].dropna()  # Removed 'timestamp'
    scaler = MinMaxScaler(feature_range=(0, 1))
    data['scaled_close'] = scaler.fit_transform(data[['close']])

    X, y = [], []
    for ticker in data['ticker'].unique():
        ticker_data = data[data['ticker'] == ticker]
        scaled_data = ticker_data['scaled_close'].values
        for i in range(look_back, len(scaled_data)):
            X.append(scaled_data[i-look_back:i])
            y.append(scaled_data[i])

    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    return X, y, scaler


# Example usage
if __name__ == "__main__":
    raw_data = load_data_from_postgres()
    X, y, scaler = prepare_data_for_model(raw_data)
