import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go


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


def plot_price_with_ma(df, ticker, price_column='Close', ma_columns=['MA10', 'MA50', 'MA100'], log_scale=False):
    """
    Plot candlestick chart with moving averages using Plotly.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with stock data (must have Open, High, Low, Close columns)
    ticker : str
        Stock ticker symbol for the title
    price_column : str
        Name of the price column to plot (default: 'Close')
    ma_columns : list
        List of MA column names to plot (default: ['MA10', 'MA50', 'MA100'])
    log_scale : bool
        If True, apply logarithmic scaling to the y-axis (default: False)

    Returns:
    --------
    plotly.graph_objects.Figure
        The created interactive figure object
    """
    fig = go.Figure()

    # Apply log transformation if requested
    if log_scale:
        df_plot = df.copy()
        df_plot['Open'] = np.log10(df['Open'])
        df_plot['High'] = np.log10(df['High'])
        df_plot['Low'] = np.log10(df['Low'])
        df_plot['Close'] = np.log10(df['Close'])
        for ma_col in ma_columns:
            if ma_col in df.columns:
                df_plot[ma_col] = np.log10(df[ma_col])
        ylabel = 'Price (log10 $)'
    else:
        df_plot = df
        ylabel = 'Price ($)'

    fig.add_trace(go.Candlestick(
        x=df_plot.index,
        open=df_plot['Open'],
        high=df_plot['High'],
        low=df_plot['Low'],
        close=df_plot['Close'],
        name=ticker,
        increasing_line_color='#26a69a',
        decreasing_line_color='#ef5350',
        increasing_fillcolor='#26a69a',
        decreasing_fillcolor='#ef5350'
    ))

    colors = ['blue', 'orange', 'purple']
    for i, ma_col in enumerate(ma_columns):
        if ma_col in df_plot.columns:
            fig.add_trace(go.Scatter(
                x=df_plot.index,
                y=df_plot[ma_col],
                name=ma_col,
                line=dict(color=colors[i % len(colors)], width=2),
                mode='lines',
                opacity=0.7
            ))

    fig.update_layout(
        title=f'{ticker} Candlestick Chart with Moving Averages{"(Log Scale)" if log_scale else ""}',
        xaxis_title='Date',
        yaxis_title=ylabel,
        hovermode='x unified',
        template='plotly_white',
        height=600,
        xaxis_rangeslider_visible=False,
        showlegend=True
    )

    return fig
