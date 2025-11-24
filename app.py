import streamlit as st
from src.utils import get_stock_data, calculate_moving_averages, plot_price_with_ma
from dataclasses import dataclass
from typing import Optional, List
import time


@dataclass
class StockConfig:
    """Configuration for stock data fetching and visualization"""
    ticker: str
    fetch_method: str
    interval: str
    ma_windows: List[int]
    log_scale: bool
    live_mode: bool = False
    update_frequency: int = 60
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

        # Live mode options
        st.subheader("Live Update Settings")
        live_mode = st.checkbox(
            "Enable Live Updates",
            value=False,
            help="Automatically refresh chart at specified intervals"
        )

        update_frequency = st.number_input(
            "Update Frequency (seconds)",
            min_value=10,
            max_value=3600,
            value=60,
            step=10,
            help="How often to refresh the data (minimum 10 seconds)",
            disabled=not live_mode
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
                live_mode=live_mode,
                update_frequency=update_frequency,
                period=period
            )
        else:
            config = StockConfig(
                ticker=ticker.strip().upper(),
                fetch_method=fetch_method,
                interval=interval,
                ma_windows=ma_windows,
                log_scale=log_scale,
                live_mode=live_mode,
                update_frequency=update_frequency,
                start_date=start_date.strftime(
                    '%Y-%m-%d') if start_date else None,
                end_date=end_date.strftime('%Y-%m-%d') if end_date else None
            )


# Display form data when submitted
if submitted:
    st.success("✅ Form submitted successfully!")

    # Validation
    if not config.ticker:
        st.error("❌ Please enter a valid ticker symbol!")
    elif config.fetch_method == "Date Range" and (config.start_date is None or config.end_date is None):
        st.error("❌ Please select both start and end dates!")
    elif config.fetch_method == "Date Range" and config.start_date >= config.end_date:
        st.error("❌ Start date must be before end date!")
    else:
        # Show loading spinner while fetching data
        with st.spinner(f"📊 Fetching data for {config.ticker}..."):
            try:
                # Fetch stock data
                if config.fetch_method == "Period":
                    df = get_stock_data(
                        config.ticker, period=config.period, interval=config.interval)
                else:
                    df = get_stock_data(config.ticker, start_date=config.start_date,
                                        end_date=config.end_date, interval=config.interval)

                if df.empty:
                    st.error(
                        f"❌ No data found for ticker '{config.ticker}'. Please check the ticker symbol and try again.")
                else:
                    # Display data info
                    st.success(
                        f"✅ Successfully fetched {len(df)} data points!")

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Data Points", len(df))
                    with col2:
                        st.metric("Start Date",
                                  df.index[0].strftime('%Y-%m-%d'))
                    with col3:
                        st.metric(
                            "End Date", df.index[-1].strftime('%Y-%m-%d'))

                    # Calculate moving averages
                    if config.ma_windows:
                        with st.spinner("📈 Calculating moving averages..."):
                            df_with_ma = calculate_moving_averages(
                                df, windows=config.ma_windows, price_column='Close')
                            ma_columns = [f'MA{w}' for w in config.ma_windows]
                    else:
                        df_with_ma = df
                        ma_columns = []

                    # Plot candlestick chart
                    st.subheader(f"📊 {config.ticker} Candlestick Chart")

                    # Create placeholders for live updates
                    chart_placeholder = st.empty()
                    data_placeholder = st.empty()

                    if config.live_mode:
                        status_placeholder = st.empty()
                        status_placeholder.info(
                            f"🔴 Live mode enabled - updating every {config.update_frequency} seconds. Refresh the page to stop.")

                    # Live update loop
                    update_count = 0
                    while True:
                        update_count += 1

                        # Fetch fresh data for live mode (skip on first iteration since we already have data)
                        if config.live_mode and update_count > 1:
                            try:
                                if config.fetch_method == "Period":
                                    df = get_stock_data(
                                        config.ticker, period=config.period, interval=config.interval)
                                else:
                                    df = get_stock_data(config.ticker, start_date=config.start_date,
                                                        end_date=config.end_date, interval=config.interval)

                                if not df.empty:
                                    # Recalculate moving averages
                                    if config.ma_windows:
                                        df_with_ma = calculate_moving_averages(
                                            df, windows=config.ma_windows, price_column='Close')
                                    else:
                                        df_with_ma = df
                            except Exception as e:
                                st.error(f"❌ Error updating data: {str(e)}")
                                break

                        # Render chart in placeholder
                        with chart_placeholder.container():
                            with st.spinner("🎨 Rendering chart..."):
                                fig = plot_price_with_ma(
                                    df_with_ma,
                                    config.ticker,
                                    price_column='Close',
                                    ma_columns=ma_columns,
                                    log_scale=config.log_scale
                                )
                                st.plotly_chart(
                                    fig, width='stretch', key=f"chart_{update_count}")

                        # Show data preview in placeholder
                        with data_placeholder.container():
                            with st.expander("📋 View Data Table"):
                                st.dataframe(df_with_ma.tail(
                                    20), width='stretch')

                        # Break loop if not in live mode
                        if not config.live_mode:
                            break

                        # Update status with last update time
                        if config.live_mode:
                            current_time = time.strftime("%H:%M:%S")
                            status_placeholder.info(
                                f"🟢 Live mode active - Last updated: {current_time} - Next update in {config.update_frequency}s")

                        # Wait before next update
                        time.sleep(config.update_frequency)

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.exception(e)

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit and yfinance")
