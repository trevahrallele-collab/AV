#!/usr/bin/env python3
"""
Stock Data Integration - Quick Reference & Examples
Copy-paste snippets for common tasks
"""

# =============================================================================
# 1. FETCH & UPDATE STOCK DATA
# =============================================================================

# Option A: Update all Big Five stocks
from fetch_stock_data import fetch_and_store_all_stocks
fetch_and_store_all_stocks()  # Pulls latest 5 years from yfinance

# Option B: Update specific stocks
from fetch_stock_data import fetch_and_store_all_stocks
fetch_and_store_all_stocks(['AAPL', 'MSFT', 'NVDA'])

# Option C: Fetch data for a single stock
from fetch_stock_data import fetch_stock_data_yfinance, save_stock_to_database
df = fetch_stock_data_yfinance('AAPL', period='5y')
save_stock_to_database('AAPL', df)

# Option D: Get database info
from fetch_stock_data import list_stock_tables, get_database_stats
list_stock_tables()  # Print all tables
stats = get_database_stats()  # Get statistics


# =============================================================================
# 2. RUN STOCK BACKTESTS
# =============================================================================

# Option A: Backtest all Big Five stocks
from stock_backtest_runner import run_all_stocks_backtest
summary = run_all_stocks_backtest()
print(summary)  # Print summary table
summary.to_csv('results.csv')  # Save to CSV

# Option B: Backtest single stock
from stock_backtest_runner import run_stock_backtest
stats, df, bt = run_stock_backtest('AAPL', cash=100_000, commission=0.001)
print(f"Return: {stats['Return [%]']:.2f}%")
print(f"Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
print(f"Win Rate: {stats['Win Rate [%]']:.2f}%")

# Option C: Custom parameters
stats, df, bt = run_stock_backtest(
    symbol='MSFT',
    cash=50_000,
    commission=0.002,
    atr_mult_sl=2.0,      # Stop loss multiplier
    rr_mult_tp=3.0,       # Take profit multiplier
    ema_length=50,        # Trend filter EMA
    ichimoku_lookback=15  # Cloud confirmation window
)

# Option D: Get backtest object and plot
stats, df, bt = run_stock_backtest('AAPL')
# Access backtest object for plotting:
# bt.plot(filename='chart.html')  # Interactive chart
# bt.orders  # List of executed orders
# bt.trades  # List of completed trades


# =============================================================================
# 3. QUERY STOCK DATA DIRECTLY
# =============================================================================

from fetch_stock_data import get_stock_data
import pandas as pd

# Get AAPL data
aapl_data = get_stock_data('AAPL')
print(aapl_data.head())  # First 5 rows
print(aapl_data.tail())  # Last 5 rows

# Filter by date range
aapl_2024 = aapl_data['2024-01-01':'2024-12-31']
print(f"2024 data: {len(aapl_2024)} rows")

# Get specific columns
opens = aapl_data['Open']
closes = aapl_data['Close']
volumes = aapl_data['Volume']

# Calculate returns
returns = aapl_data['Close'].pct_change()
print(f"Average daily return: {returns.mean():.4f}")


# =============================================================================
# 4. GENERATE REPORTS & VISUALIZATIONS
# =============================================================================

# Generate all comparison reports
from create_backtest_comparison import load_backtest_results, create_comparison_plots, create_asset_class_summary, create_html_report

stock_df, forex_df, all_df = load_backtest_results()
create_comparison_plots(stock_df, forex_df, all_df)
create_asset_class_summary(all_df)
create_html_report(all_df, stock_df, forex_df)
print("Reports generated:")
print("  - backtest_comparison.png")
print("  - asset_class_summary.png")
print("  - backtest_analysis_report.html")


# =============================================================================
# 5. ADVANCED BACKTEST ANALYSIS
# =============================================================================

from stock_backtest_runner import run_stock_backtest
import pandas as pd

# Run backtest and analyze results
stats, df, bt = run_stock_backtest('AAPL')

# Access statistics
print("=== STRATEGY METRICS ===")
print(f"Total Return: {stats['Return [%]']:.2f}%")
print(f"Annual Return: {stats['Return (ann.) [%]']:.2f}%")
print(f"Max Drawdown: {stats['Max. Drawdown [%]']:.2f}%")
print(f"Win Rate: {stats['Win Rate [%]']:.2f}%")
print(f"Best Trade: {stats['Best Trade [%]']:.2f}%")
print(f"Worst Trade: {stats['Worst Trade [%]']:.2f}%")
print(f"Profit Factor: {stats['Profit Factor']:.2f}")
print(f"Sharpe Ratio: {stats['Sharpe Ratio']:.2f}")
print(f"Sortino Ratio: {stats['Sortino Ratio']:.2f}")

# Access trades
print(f"\n=== TRADES ({len(bt.trades)}) ===")
for i, trade in enumerate(bt.trades[:5], 1):  # First 5 trades
    print(f"{i}. Entry: {trade.entry_time}, Exit: {trade.exit_time}, PnL: {trade.pl:.2f}")

# Access dataframe with all indicators
print(f"\n=== INDICATOR DATA ===")
print(df[['Close', 'Tenkan', 'Kijun', 'Senkou_A', 'Senkou_B', 'EMA', 'signal']].head())


# =============================================================================
# 6. DATABASE OPERATIONS
# =============================================================================

from database import save_to_database, load_from_database, list_tables
from config import STOCKS_DB_PATH

# Load data from database
df = load_from_database('AAPL_daily', STOCKS_DB_PATH)
print(f"Loaded {len(df)} rows of AAPL data")

# Save data to database
df.to_sql('CUSTOM_DATA_daily', con=f'sqlite:///{STOCKS_DB_PATH}', if_exists='replace')

# List all tables
tables = list_tables(STOCKS_DB_PATH)
print(f"Database tables: {tables}")


# =============================================================================
# 7. STRATEGY OPTIMIZATION
# =============================================================================

from stock_backtest_runner import run_stock_backtest
import itertools

# Test different parameter combinations
ema_lengths = [50, 100, 150]
atr_mults = [1.0, 1.5, 2.0]
results = []

for ema_len, atr_mult in itertools.product(ema_lengths, atr_mults):
    try:
        stats, df, bt = run_stock_backtest(
            'AAPL',
            ema_length=ema_len,
            atr_mult_sl=atr_mult
        )
        results.append({
            'ema_length': ema_len,
            'atr_mult': atr_mult,
            'return': stats['Return [%]'],
            'sharpe': stats['Sharpe Ratio'],
            'trades': stats['# Trades']
        })
    except Exception as e:
        print(f"Failed: EMA={ema_len}, ATR={atr_mult}: {e}")

# Find best parameters
best = max(results, key=lambda x: x['return'])
print(f"Best parameters: EMA={best['ema_length']}, ATR={best['atr_mult']}")
print(f"Return: {best['return']:.2f}%")


# =============================================================================
# 8. COMPARING MULTIPLE STOCKS
# =============================================================================

from stock_backtest_runner import run_all_stocks_backtest
import pandas as pd

# Run backtests for all stocks
summary = run_all_stocks_backtest(['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA'])

# Sort by return
top_performers = summary.sort_values('Return [%]', ascending=False)
print("\n=== TOP PERFORMERS ===")
print(top_performers[['Symbol', 'Return [%]', 'Win Rate [%]', '# Trades']])

# Filter by criteria
high_win_rate = summary[summary['Win Rate [%]'] > 50]
print(f"\nHigh win rate stocks (>50%): {len(high_win_rate)}")
print(high_win_rate[['Symbol', 'Win Rate [%]', 'Profit Factor']])


# =============================================================================
# 9. FILE PATHS & CONFIGURATION
# =============================================================================

from config import STOCKS_DB_PATH, STOCK_SYMBOLS

print(f"Stock database: {STOCKS_DB_PATH}")
print(f"Stock symbols: {STOCK_SYMBOLS}")

# Database location
import os
db_path = STOCKS_DB_PATH.replace('sqlite:///', '')
print(f"Database file: {os.path.abspath(db_path)}")


# =============================================================================
# 10. ERROR HANDLING
# =============================================================================

from stock_backtest_runner import run_stock_backtest
from fetch_stock_data import get_stock_data

# Safe backtest run
try:
    stats, df, bt = run_stock_backtest('AAPL')
except Exception as e:
    print(f"Backtest failed: {e}")
    print("Check if stock data exists in database")

# Safe data fetch
try:
    df = get_stock_data('UNKNOWN')
except Exception as e:
    print(f"Data fetch failed: {e}")
    print("Stock may not exist in database")


# =============================================================================
# USEFUL TERMINAL COMMANDS
# =============================================================================

"""
# Update all stock data
python fetch_stock_data.py

# Run all backtests
python stock_backtest_runner.py

# Generate comparison reports
python create_backtest_comparison.py

# Check database
sqlite3 stocks.db ".tables"
sqlite3 stocks.db ".schema AAPL_daily"
sqlite3 stocks.db "SELECT COUNT(*) FROM AAPL_daily;"

# Python interactive shell
python3
>>> from fetch_stock_data import get_stock_data
>>> df = get_stock_data('AAPL')
>>> print(df.describe())
>>> exit()
"""
