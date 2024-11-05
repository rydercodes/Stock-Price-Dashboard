#!/bin/bash

# Wait for the database to be ready
until pg_isready -h db -p 5432 -U jaber; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 2
done

# Run data_fetching.py to create and populate the table
python data_fetching.py

# Start the Streamlit app
streamlit run dashboard.py --server.port=8501 --server.address=0.0.0.0
