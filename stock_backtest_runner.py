"""
Unified Backtest Runner for Stocks and Forex
Runs backtests for multiple stock tickers similar to forex pairs
"""

import pandas as pd
from sqlalchemy import create_engine
from backtesting import Backtest

from ichimoku import (
    fetch_data_from_database,
    add_ichimoku,
    add_ema_signal,
    create_ichimoku_signal,
    TENKAN, KIJUN, SENKOU_B, ATR_LEN
)
from strategy import SignalStrategy
from config import STOCKS_DB_PATH, STOCK_SYMBOLS


def run_stock_backtest(
    symbol: str,
    db_path: str = STOCKS_DB_PATH,
    cash: float = 100_000,
    commission: float = 0.001,
    atr_mult_sl: float = 1.5,
    rr_mult_tp: float = 2.0,
    ema_length: int = 100,
    ema_back_candles: int = 7,
    ichimoku_lookback: int = 10,
    ichimoku_min_confirm: int = 5,
    show_plot: bool = False,
):
    """
    Run a complete Ichimoku backtest for a stock using data from SQLite database.
    
    Args:
        symbol: Stock ticker (e.g., 'AAPL')
        db_path: Path to stocks database
        cash: Initial cash for backtest
        commission: Commission per trade (decimal, e.g., 0.001 = 0.1%)
        atr_mult_sl: ATR multiplier for stop-loss
        rr_mult_tp: Risk-reward ratio for take-profit
        ema_length: EMA period for trend filter
        ema_back_candles: Number of lookback candles for EMA signal
        ichimoku_lookback: Lookback window for cloud confirmation
        ichimoku_min_confirm: Min bars above/below cloud required
        show_plot: If True, render interactive plot
    
    Returns:
        tuple: (stats, df, bt) where
            - stats: Backtest statistics
            - df: DataFrame with all indicators and signals
            - bt: Backtest object
    """
    print(f"\n{'='*70}")
    print(f"Running Ichimoku Backtest: {symbol}")
    print(f"{'='*70}")
    
    # Fetch and prepare data
    print(f"📊 Fetching {symbol} from database...")
    try:
        engine = create_engine(db_path)
        table_name = f"{symbol}_daily"
        query = f"SELECT * FROM '{table_name}' ORDER BY date"
        df = pd.read_sql(query, engine, index_col='date', parse_dates=['date'])
        
        # Standardize column names
        df.columns = df.columns.str.capitalize()
        
        print(f"   Loaded {len(df)} rows")
    except Exception as e:
        print(f"   ❌ Error loading data: {str(e)}")
        raise
    
    # Add Ichimoku indicators
    print(f"📈 Adding Ichimoku Cloud indicators...")
    df = add_ichimoku(df, tenkan=TENKAN, kijun=KIJUN, senkou_b=SENKOU_B)
    
    # Add EMA trend filter
    print(f"📈 Adding EMA trend filter (length={ema_length})...")
    df = add_ema_signal(df, ema_length=ema_length, back_candles=ema_back_candles)
    
    # Create trading signals
    print(f"📊 Creating Ichimoku + EMA signals...")
    df = create_ichimoku_signal(
        df,
        lookback_window=ichimoku_lookback,
        min_confirm=ichimoku_min_confirm
    )
    
    # Drop NaN rows
    df = df.dropna(subset=["signal", "ATR"])
    print(f"   {len(df)} rows after dropping NaN")
    
    # Run backtest
    print(f"🎯 Running backtest with {len(df)} candles...")
    bt = Backtest(
        df,
        SignalStrategy,
        cash=cash,
        commission=commission,
        trade_on_close=True,
        exclusive_orders=True,
        margin=1/10,
    )
    
    # Run with parameters
    stats = bt.run(atr_mult_sl=atr_mult_sl, rr_mult_tp=rr_mult_tp)
    
    # Save equity curve chart as HTML
    chart_filename = f"{symbol}_daily_equity.html"
    try:
        bt.plot(filename=chart_filename)
        print(f"✅ Equity chart saved to {chart_filename}")
    except Exception as e:
        print(f"⚠️ Could not save chart for {symbol}: {e}")
    
    # Print results
    print(f"\n✅ Backtest Results for {symbol}:")
    print(f"   Return: {stats.get('Return [%]', 0):.2f}%")
    print(f"   Max Drawdown: {stats.get('Max. Drawdown [%]', 0):.2f}%")
    print(f"   Win Rate: {stats.get('Win Rate [%]', 0):.2f}%")
    print(f"   # Trades: {stats.get('# Trades', 0)}")
    print(f"   Exposure Time: {stats.get('Exposure Time [%]', 0):.2f}%")
    
    return stats, df, bt


def run_all_stocks_backtest(
    symbols: list = None,
    db_path: str = STOCKS_DB_PATH,
    cash: float = 100_000,
    commission: float = 0.001,
):
    """
    Run backtests for all stock symbols and create summary.
    
    Args:
        symbols: List of stock tickers (default: STOCK_SYMBOLS from config)
        db_path: Path to stocks database
        cash: Initial cash for backtest
        commission: Commission per trade
    
    Returns:
        DataFrame with summary results for all symbols
    """
    if symbols is None:
        symbols = STOCK_SYMBOLS
    
    results = []
    
    print(f"\n{'='*70}")
    print(f"🚀 RUNNING BACKTESTS FOR ALL STOCKS")
    print(f"{'='*70}")
    
    for i, symbol in enumerate(symbols, 1):
        print(f"\n[{i}/{len(symbols)}] {symbol}...")
        try:
            stats, df, bt = run_stock_backtest(
                symbol,
                db_path=db_path,
                cash=cash,
                commission=commission
            )
            
            results.append({
                'Symbol': symbol,
                'Return [%]': stats.get('Return [%]', 0),
                'Buy & Hold Return [%]': stats.get('Buy & Hold Return [%]', 0),
                'Max. Drawdown [%]': stats.get('Max. Drawdown [%]', 0),
                'Win Rate [%]': stats.get('Win Rate [%]', 0),
                'Profit Factor': stats.get('Profit Factor', 0),
                'Sharpe Ratio': stats.get('Sharpe Ratio', 0),
                '# Trades': stats.get('# Trades', 0),
                'Exposure Time [%]': stats.get('Exposure Time [%]', 0),
            })
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results.append({
                'Symbol': symbol,
                'Error': str(e)
            })
    
    # Create summary DataFrame
    summary_df = pd.DataFrame(results)
    
    # Print summary table
    print(f"\n{'='*70}")
    print(f"📊 BACKTEST SUMMARY")
    print(f"{'='*70}")
    print(summary_df.to_string(index=False))
    print(f"{'='*70}\n")
    
    return summary_df


def create_stock_comparison_csv(symbols: list = None, output_file: str = "stock_backtest_summary.csv"):
    """
    Create and save backtest summary CSV for all stocks.
    
    Args:
        symbols: List of stock tickers
        output_file: Output CSV filename
    """
    summary = run_all_stocks_backtest(symbols)
    summary.to_csv(output_file, index=False)
    print(f"✅ Summary saved to {output_file}")


if __name__ == "__main__":
    # Run backtests for all Big Five stocks
    create_stock_comparison_csv(STOCK_SYMBOLS)
