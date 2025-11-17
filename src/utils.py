import yfinance as yf
import matplotlib.pyplot as plt


def get_stock_data(ticker, start_date=None, end_date=None, period='1mo', interval='1d'):
    """
    Fetch stock data from yfinance.

    Parameters:
    -----------
    ticker : str
        Stock ticker symbol (e.g., 'AAPL', 'MSFT')
    start_date : str, optional
        Start date in 'YYYY-MM-DD' format
    end_date : str, optional
        End date in 'YYYY-MM-DD' format
    period : str
        Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        Default: 1mo
        Either use period parameter or use start and end
    interval : str
        Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        Default: 1d
        Intraday data cannot extend last 60 days

    Returns:
    --------
    pd.DataFrame
        DataFrame with stock data
    """
    # If start_date and end_date are provided, use them; otherwise use period
    if start_date and end_date:
        data = yf.download(ticker, start=start_date,
                           end=end_date, interval=interval)
    else:
        data = yf.download(ticker, period=period, interval=interval)

    # Flatten MultiIndex columns if present (yfinance sometimes returns MultiIndex)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data


def calculate_moving_averages(df, windows=[10, 50, 100], price_column='Close'):
    """
    Calculate moving averages for specified windows.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with stock data
    windows : list
        List of window sizes for moving averages (default: [10, 50, 100])
    price_column : str
        Name of the column to calculate MA on (default: 'Close')

    Returns:
    --------
    pd.DataFrame
        DataFrame with added MA columns
    """
    df_copy = df.copy()

    for window in windows:
        column_name = f'MA{window}'
        df_copy[column_name] = df_copy[price_column].rolling(
            window=window).mean()

    return df_copy


def plot_price_with_ma(df, ticker, price_column='Close', ma_columns=['MA10', 'MA50', 'MA100']):
    """
    Plot stock price with moving averages.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with stock data and moving averages
    ticker : str
        Stock ticker symbol for the title
    price_column : str
        Name of the price column to plot (default: 'Close')
    ma_columns : list
        List of MA column names to plot (default: ['MA10', 'MA50', 'MA100'])

    Returns:
    --------
    matplotlib.figure.Figure
        The created figure object
    """
    fig, ax = plt.subplots(figsize=(14, 7))

    # Plot close price
    ax.plot(df.index, df[price_column],
            label=f'{ticker} Price', linewidth=2, color='black')

    # Plot moving averages with different colors
    colors = ['blue', 'orange', 'green']
    for i, ma_col in enumerate(ma_columns):
        if ma_col in df.columns:
            ax.plot(df.index, df[ma_col], label=ma_col, linewidth=1.5,
                    color=colors[i % len(colors)], alpha=0.8)

    ax.set_title(f'{ticker} Stock Price with Moving Averages',
                 fontsize=16, fontweight='bold')
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price ($)', fontsize=12)
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig
