import streamlit as st
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class StockConfig:
    """Configuration for stock data fetching and visualization"""
    ticker: str
    fetch_method: str
    interval: str
    ma_windows: List[int]
    log_scale: bool
    period: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


# Page configuration
st.set_page_config(
    page_title="Stock Market Analysis",
    page_icon="📈",
    layout="wide"
)

# Main title
st.title("📈 Stock Market Analysis with Moving Averages")

# Sidebar
st.sidebar.header("About")
st.sidebar.info(
    """
    This app provides real-time stock market analysis with:
    - Candlestick charts
    - Moving averages (MA10, MA50, MA100)
    - Live price updates
    - Logarithmic scaling option
    """
)

# Main content area
st.header("Stock Data Configuration")

# Data fetch method selection (outside form for dynamic updates)
fetch_method = st.radio(
    "Data Fetch Method",
    options=["Period", "Date Range"],
    help="Choose how to fetch data",
    horizontal=True
)

# Create form for data input
with st.form("stock_data_form"):
    col1, col2 = st.columns(2)

    with col1:
        ticker = st.text_input(
            "Stock Ticker Symbol",
            value="AAPL",
            help="Enter stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"
        )

        if fetch_method == "Period":
            period = st.selectbox(
                "Period",
                options=["1d", "5d", "1mo", "3mo", "6mo",
                         "1y", "2y", "5y", "10y", "ytd", "max"],
                index=5,  # Default to "1y"
                help="Select time period for data"
            )
            start_date = None
            end_date = None
        else:
            period = None
            start_date = st.date_input(
                "Start Date",
                value=None,
                help="Select start date"
            )
            end_date = st.date_input(
                "End Date",
                value=None,
                help="Select end date"
            )

    with col2:
        interval = st.selectbox(
            "Interval",
            options=["1m", "2m", "5m", "15m", "30m", "60m",
                     "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"],
            index=8,  # Default to "1d"
            help="Data interval (intraday data cannot extend last 60 days)"
        )

        # Moving average windows
        st.subheader("Moving Averages")
        ma_windows = st.multiselect(
            "Select MA Windows",
            options=[5, 10, 20, 50, 100, 200],
            default=[10, 50, 100],
            help="Select moving average windows to display"
        )

        # Logarithmic scale option
        log_scale = st.checkbox(
            "Use Logarithmic Scale",
            value=False,
            help="Apply log scale to y-axis"
        )

    # Submit button
    submitted = st.form_submit_button("Fetch Data & Plot", type="primary")

    # Create config object when form is submitted
    if submitted:
        if fetch_method == "Period":
            config = StockConfig(
                ticker=ticker.strip().upper(),
                fetch_method=fetch_method,
                interval=interval,
                ma_windows=ma_windows,
                log_scale=log_scale,
                period=period
            )
        else:
            config = StockConfig(
                ticker=ticker.strip().upper(),
                fetch_method=fetch_method,
                interval=interval,
                ma_windows=ma_windows,
                log_scale=log_scale,
                start_date=start_date.strftime(
                    '%Y-%m-%d') if start_date else None,
                end_date=end_date.strftime('%Y-%m-%d') if end_date else None
            )


# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit and yfinance")

