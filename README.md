
# Stock Price and Moving Average Dashboard

This project is a web-based dashboard that allows users to visualize stock prices and their moving averages for selected stocks. It fetches historical stock data from Yahoo Finance, stores it in a PostgreSQL database, and displays interactive charts using Streamlit. The application is containerized using Docker and orchestrated with Docker Compose.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Data Fetching**: Retrieves historical stock data for predefined ticker symbols over the past year at hourly intervals.
- **Database Storage**: Stores the fetched data in a PostgreSQL database running inside a Docker container.
- **Data Transformation**: Calculates the moving average of closing prices using SQL window functions.
- **Interactive Dashboard**: Provides an interactive Streamlit dashboard for visualizing stock prices and moving averages.
- **Data Table Display**: Displays the underlying data in a table format for detailed analysis.
- **Dynamic Ticker Selection**: Allows users to select different ticker symbols to update the charts and data.

## Architecture

The application consists of two main services defined in `docker-compose.yml`:

1. **Database Service (`db`)**:
   - Runs a PostgreSQL database inside a Docker container.
   - Stores stock data in the `raw_stock_data` table.
2. **Application Service (`app`)**:
   - Runs the Streamlit application inside a Docker container.
   - Fetches data using `data_fetching.py` and displays the dashboard via `dashboard.py`.
   - Waits for the database to be ready before starting the application.

## Technologies Used

- **Python 3.11**
- **Streamlit**: For building the interactive web dashboard.
- **Pandas**: For data manipulation and analysis.
- **yfinance**: For fetching historical stock data from Yahoo Finance.
- **SQLAlchemy**: For database interactions.
- **PostgreSQL**: For data storage.
- **Docker & Docker Compose**: For containerization and orchestration.

## Prerequisites

- **Docker**: Make sure Docker is installed on your machine.
- **Docker Compose**: Ensure you have Docker Compose installed.
- **Git**: Optional, for cloning the repository.

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/stock-price-dashboard.git
cd stock-price-dashboard
```

**Note**: Replace `https://github.com/yourusername/stock-price-dashboard.git` with the actual URL of your repository.

### 2. Build and Start the Docker Containers

Use Docker Compose to build and run the application:

```bash
docker-compose up --build
```

This command will:

- Build the Docker images for both services (`app` and `db`).
- Start the services defined in `docker-compose.yml`.

### 3. Wait for the Application to Initialize

- The `app` service will:
  - Wait for the `db` service to be ready.
  - Run `data_fetching.py` to fetch and store stock data.
  - Start the Streamlit dashboard.

You can monitor the logs to see the progress:

```bash
docker-compose logs -f
```

### 4. Access the Dashboard

Once the containers are running and the initialization is complete, open your web browser and navigate to:

```
http://localhost:8501
```

You should see the **Stock Price and Moving Average Dashboard**.

## Usage

### Selecting a Ticker Symbol

- Use the dropdown menu labeled **"Choose a ticker symbol:"** to select a stock (e.g., AAPL, MSFT, GOOGL).

### Viewing the Data Table

- The dashboard displays a data table showing:
  - `datetime`: The timestamp of each data point.
  - `close`: The closing price of the stock.
  - `moving_avg`: The moving average of the closing price over the past 10 periods.

### Interacting with the Chart

- The line chart visualizes the `close` price and `moving_avg` over time.
- Hover over the chart to see exact values.
- The chart updates automatically when a different ticker is selected.

### Exploring Different Stocks

- Select different ticker symbols to compare stock performance and trends.

## Project Structure

```
stock-price-dashboard/
├── dashboard.py
├── data_fetching.py
├── entrypoint.sh
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

- **dashboard.py**: Contains the Streamlit application code.
- **data_fetching.py**: Script to fetch stock data and populate the database.
- **entrypoint.sh**: Entrypoint script for the Docker container; waits for the database and initializes the application.
- **requirements.txt**: Lists Python dependencies.
- **Dockerfile**: Defines the Docker image for the `app` service.
- **docker-compose.yml**: Configures Docker services and networking.
- **README.md**: Project documentation.

## Troubleshooting

### Common Issues and Solutions

#### 1. `UndefinedTable` Error

- **Problem**: The application cannot find the `raw_stock_data` table.
- **Solution**: Ensure that `data_fetching.py` runs successfully and populates the database. Check the logs for any errors during data fetching.

#### 2. `psycopg2.errors.UndefinedTable` Exception

- **Problem**: Occurs when the SQL query references a table that doesn't exist.
- **Solution**: Verify that the table creation in `data_fetching.py` is executed without errors. The `create_table_if_not_exists` function should properly check and create the table.

#### 3. Docker Containers Not Reflecting Code Changes

- **Problem**: Changes made to the code are not visible in the running application.
- **Solution**: Rebuild the Docker images using the `--build` flag:

  ```bash
  docker-compose down
  docker-compose up --build
  ```

#### 4. `pg_isready: command not found`

- **Problem**: The `pg_isready` command is not available in the Docker container.
- **Solution**: Ensure that the PostgreSQL client is installed in the `Dockerfile`:

  ```dockerfile
  RUN apt-get update && apt-get install -y postgresql-client
  ```

#### 5. Database Connection Issues

- **Problem**: The application cannot connect to the PostgreSQL database.
- **Solution**: Verify that the connection string in your Python scripts matches the database credentials in `docker-compose.yml`.

### Checking Logs

- **Application Logs**:

  ```bash
  docker-compose logs app
  ```

- **Database Logs**:

  ```bash
  docker-compose logs db
  ```

### Accessing the Containers

- **App Container**:

  ```bash
  docker-compose exec app bash
  ```

- **Database Container**:

  ```bash
  docker-compose exec db psql -U jaber -d stock_data
  ```

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

   Click the "Fork" button at the top right of the repository page.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/rydercodes/Stock-Price-Dashboard.git
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**

   - Ensure code quality and consistency.
   - Update documentation if necessary.

5. **Commit and Push**

   ```bash
   git commit -m "Add your commit message here"
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**

   Go to your fork on GitHub and click the "Compare & pull request" button.

## License

This project is licensed under the [MIT License](LICENSE).
