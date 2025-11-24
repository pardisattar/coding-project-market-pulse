# Stock Market Analysis Dashboard

A real-time stock market analysis application built with Streamlit that provides interactive visualization of stock price movements with technical indicators. This project fetches live stock data using the yfinance API and displays candlestick charts with customizable moving averages. Users can analyze historical data or enable live updates to monitor stock prices in real-time.

The application allows users to configure data fetching methods (by period or custom date range), select various time intervals, and apply multiple moving averages for technical analysis. The live update feature automatically refreshes the chart at user-defined intervals, making it suitable for active market monitoring.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pardisattar/coding-project-market-pulse.git
cd coding-project-market-pulse
```

2. Create a virtual environment:
```bash
python -m venv .venv
```

3. Activate the virtual environment:
   - On Windows:
   ```bash
   .venv\Scripts\activate
   ```
   - On macOS/Linux:
   ```bash
   source .venv/bin/activate
   ```

4. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. The application will open in your default web browser at `http://localhost:8501`

3. Configure your stock analysis:
   - Enter a stock ticker symbol (e.g., AAPL, MSFT, GOOGL)
   - Choose data fetch method: Period (1d, 1mo, 1y, etc.) or Date Range
   - Select data interval (1m, 1h, 1d, 1wk, etc.)
   - Choose moving average windows (5, 10, 20, 50, 100, 200)
   - Optionally enable logarithmic scale for price axis
   - Enable live updates and set refresh frequency if desired

4. Click "Fetch Data & Plot" to display the candlestick chart with moving averages

5. View the interactive chart and explore the data table in the expandable section below

Example configuration for analyzing Apple stock over the past year with daily data:
- Ticker: AAPL
- Fetch Method: Period
- Period: 1y
- Interval: 1d
- Moving Averages: 10, 50, 100
- Live Updates: Disabled

### Jupyter Notebook Example

A comprehensive example notebook is available at `notebooks/main.ipynb` that demonstrates programmatic usage of the core utility functions. The notebook provides a step-by-step walkthrough including:

- Importing the utility functions from the src module
- Fetching stock data for a specific ticker symbol
- Calculating moving averages with customizable window sizes
- Generating interactive candlestick charts with Plotly
- Applying logarithmic scaling to visualize long-term price trends

This notebook is useful for users who want to integrate the stock analysis functions into their own Python scripts or Jupyter workflows without using the Streamlit interface.
