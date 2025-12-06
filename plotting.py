"""
Plotting module for financial data visualization.
Uses Plotly for interactive candlestick charts and other visualizations.
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_candlestick(df: pd.DataFrame, title: str = "Candlestick Chart") -> None:
    """
    Create and display an interactive candlestick chart.
    
    Args:
        df: DataFrame with columns: open, high, low, close, and datetime index
        title: Title of the chart
    """
    # Ensure index is datetime
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    
    fig.update_layout(
        title=title,
        yaxis_title="Price",
        xaxis_title="Date",
        xaxis_rangeslider_visible=False,
        template="plotly_white",
        hovermode="x unified"
    )
    
    fig.show()


def plot_price_line(df: pd.DataFrame, title: str = "Price Chart") -> None:
    """
    Create and display a line chart of closing prices.
    
    Args:
        df: DataFrame with columns: close, and datetime index
        title: Title of the chart
    """
    # Ensure index is datetime
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['close'],
        mode='lines',
        name='Close Price',
        line=dict(color='blue', width=2)
    ))
    
    fig.update_layout(
        title=title,
        yaxis_title="Price",
        xaxis_title="Date",
        template="plotly_white",
        hovermode="x unified"
    )
    
    fig.show()


def plot_ohlc(df: pd.DataFrame, title: str = "OHLC Chart") -> None:
    """
    Create and display an OHLC (Open-High-Low-Close) bar chart.
    
    Args:
        df: DataFrame with columns: open, high, low, close, and datetime index
        title: Title of the chart
    """
    # Ensure index is datetime
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    
    fig = go.Figure(data=[go.Ohlc(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    
    fig.update_layout(
        title=title,
        yaxis_title="Price",
        xaxis_title="Date",
        xaxis_rangeslider_visible=False,
        template="plotly_white",
        hovermode="x unified"
    )
    
    fig.show()


def plot_multiple_candlesticks(data_dict: dict, title: str = "Multiple Instruments") -> None:
    """
    Create candlestick charts for multiple instruments in subplots.
    
    Args:
        data_dict: Dictionary with format {instrument_name: dataframe}
        title: Title of the chart
    """
    num_pairs = len(data_dict)
    fig = make_subplots(
        rows=num_pairs, 
        cols=1,
        subplot_titles=list(data_dict.keys()),
        shared_xaxes=False
    )
    
    for idx, (name, df) in enumerate(data_dict.items(), 1):
        # Ensure index is datetime
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name=name
            ),
            row=idx, col=1
        )
    
    fig.update_layout(
        title=title,
        height=300 * num_pairs,
        template="plotly_white",
        hovermode="x unified"
    )
    
    fig.show()


def save_candlestick_html(df: pd.DataFrame, filename: str, title: str = "Candlestick Chart") -> None:
    """
    Create a candlestick chart and save it as an HTML file.
    
    Args:
        df: DataFrame with columns: open, high, low, close, and datetime index
        filename: Output HTML filename
        title: Title of the chart
    """
    # Ensure index is datetime
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    
    fig.update_layout(
        title=title,
        yaxis_title="Price",
        xaxis_title="Date",
        xaxis_rangeslider_visible=False,
        template="plotly_white",
        hovermode="x unified"
    )
    
    fig.write_html(filename)
    print(f"✅ Chart saved to {filename}")


def plot_equity_curve(equity_series, title: str = "Equity Curve", filename: str = None, show: bool = True):
    """
    Plot an equity curve (P/L over time) and optionally save to an HTML file.

    Args:
        equity_series: Pandas Series or array-like of equity values (index should be datetime)
        title: Chart title
        filename: If provided, write the interactive chart to this HTML file
        show: If True, render the figure immediately
    Returns:
        plotly Figure
    """
    import pandas as pd
    import plotly.graph_objects as go

    if not isinstance(equity_series, pd.Series):
        try:
            equity_series = pd.Series(equity_series)
        except Exception:
            raise ValueError("equity_series must be a pandas Series or array-like")

    # Ensure datetime index if possible
    if not isinstance(equity_series.index, pd.DatetimeIndex):
        try:
            equity_series.index = pd.to_datetime(equity_series.index)
        except Exception:
            pass

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=equity_series.index,
        y=equity_series.values,
        mode='lines',
        name='Equity',
        line=dict(color='green', width=2)
    ))

    # Draw zero (starting) line if useful
    fig.add_hline(y=equity_series.iloc[0] if len(equity_series) else 0, line=dict(color='gray', dash='dash'), annotation_text='Start')

    fig.update_layout(
        title=title,
        xaxis_title='Time',
        yaxis_title='Equity ($)',
        template='plotly_white',
        hovermode='x unified',
    )

    if filename:
        fig.write_html(filename)
        print(f"✅ Equity chart saved to {filename}")

    if show:
        fig.show()

    return fig
