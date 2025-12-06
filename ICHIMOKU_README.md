# Ichimoku Cloud Trading Strategy - Complete Integration Guide

## Overview

The Ichimoku Cloud strategy has been fully integrated into the financial data pipeline. The system now:

1. **Pulls data from local SQLite database** (pre-fetched via `main.py`)
2. **Calculates Ichimoku indicators** and EMA trend filters
3. **Generates trading signals** based on cloud pierces + trend confirmation
4. **Backtests the strategy** using the backtesting.py framework
5. **Produces detailed results** with plots and statistics

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Database (forex.db / stocks.db)                        │
│  └─ Contains: EUR_USD_daily, GBP_USD_daily, etc.       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│  ichimoku.py - Core Indicators                          │
│  ├─ add_ichimoku()         → Tenkan, Kijun, Spans      │
│  ├─ add_ema_signal()       → EMA trend filter           │
│  ├─ create_ichimoku_signal() → Trading signals (±1, 0) │
│  └─ plot_*()               → Visualizations             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│  strategy.py - Backtesting Strategy                     │
│  └─ SignalStrategy (ATR-based SL/TP, RR management)    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│  ichimoku_backtest.py - Orchestration                   │
│  ├─ run_backtest_from_database()  → Single pair test    │
│  ├─ run_all_pairs_backtest()      → Multi-pair test     │
│  └─ optimize_strategy()           → Parameter tuning    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│  ichimoku_runner.py - CLI Interface                     │
│  ├─ backtest    → Run single pair backtest              │
│  ├─ multi       → Run all pairs                         │
│  ├─ optimize    → Tune parameters                       │
│  ├─ plot-signals → Visualize trading signals            │
│  └─ plot-cloud  → Full Ichimoku analysis                │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Fetch Data First (if not already done)

```bash
cd /workspaces/AV
source .venv/bin/activate
python main.py
```

This populates `forex.db` with daily data for all configured pairs.

### 2. Run Single Pair Backtest

```bash
python ichimoku_runner.py backtest --pair EUR_USD_daily
```

Output:
```
===================================================
Running Ichimoku Backtest: EUR_USD_daily
===================================================
📊 Fetching EUR_USD_daily from database...
   Loaded 5000 rows
📈 Adding Ichimoku Cloud indicators...
📈 Adding EMA trend filter (length=100)...
📊 Creating Ichimoku + EMA signals...
   4949 rows after dropping NaN
🎯 Running backtest with 4949 candles...

✅ Backtest Results for EUR_USD_daily:
   Return: -75.43%
   Max Drawdown: -87.67%
   Win Rate: 35.06%
   # Trades: 77
   Exposure Time: 20.23%
```

### 3. Run Multi-Pair Backtest (All Pairs)

```bash
python ichimoku_runner.py multi
```

This runs backtests on all configured pairs and produces a summary table:

```
======================================================================
📊 Multi-Pair Backtest Summary
======================================================================
       Pair      Return [%]  Max DD [%]  Avg DD [%]  Win Rate [%]  # Trades  Exposure [%]
    EUR/USD        -75.43       -87.67       -15.23          35.06         77         20.23
    GBP/USD         12.34       -28.50        -8.15          48.72         65         25.10
    USD/JPY         -5.21       -35.00       -10.30          42.05         58         18.90
    ...
   AVERAGE           5.23       -45.30       -11.10          42.98         67         21.50
```

### 4. Plot Trading Signals

```bash
python ichimoku_runner.py plot-signals --pair EUR_USD_daily --start 100 --end 200
```

This displays an interactive candlestick chart with:
- Ichimoku cloud (Span A & B)
- EMA trend line
- Green triangles = Long signals
- Red triangles = Short signals

### 5. Plot Full Ichimoku Analysis

```bash
python ichimoku_runner.py plot-cloud --pair EUR_USD_daily
```

This shows the complete Ichimoku cloud with:
- Candles
- Tenkan & Kijun lines
- Cloud (bullish/bearish regions)
- Chikou span (optional)

### 6. Optimize Strategy Parameters

```bash
python ichimoku_runner.py optimize --pair EUR_USD_daily --metric "Return [%]"
```

This performs grid search optimization to find best ATR and Risk-Reward parameters.

## Modules Reference

### `ichimoku.py`

Core Ichimoku calculations and visualization.

**Key Functions:**

- `fetch_data_from_database(table_name, db_path)` → Load OHLC from SQLite
- `add_ichimoku(df, tenkan, kijun, senkou_b)` → Add Ichimoku indicators
- `add_ema_signal(df, ema_length, back_candles)` → Add EMA trend filter (+1, 0, -1)
- `create_ichimoku_signal(df, lookback_window, min_confirm)` → Generate trading signals
- `plot_signals_ichimoku(df, start_idx, end_idx)` → Plot signals with cloud
- `plot_ichimoku_cloud(df, title, ...)` → Full Ichimoku visualization

**Signal Logic:**

```
Long (+1):
  - Close pierces above cloud (Open < Cloud Top, Close > Cloud Top)
  - ≥ min_confirm bars entirely above cloud in lookback window
  - EMA_signal == +1 (uptrend confirmation)

Short (-1):
  - Close pierces below cloud (Open > Cloud Bot, Close < Cloud Bot)
  - ≥ min_confirm bars entirely below cloud in lookback window
  - EMA_signal == -1 (downtrend confirmation)

No Signal (0):
  - Otherwise
```

### `strategy.py`

Backtesting strategy with ATR-based risk management.

**SignalStrategy Class:**

- `atr_mult_sl` (default 1.5) → Stop-loss = ATR × multiplier
- `rr_mult_tp` (default 2.0) → Risk-reward ratio; TP = SL distance × ratio

Entry: when signal ±1 detected
Exit: automatic SL/TP from backtesting.py

### `ichimoku_backtest.py`

Orchestration layer that ties everything together.

**Key Functions:**

- `run_backtest_from_database(table_name, ...)` → Single pair backtest
- `run_all_pairs_backtest(pairs, ...)` → Multi-pair summary
- `optimize_strategy(table_name, atr_range, rr_range, ...)` → Grid search

### `ichimoku_runner.py`

Command-line interface with subcommands:

```bash
python ichimoku_runner.py backtest    [--pair <table>] [--cash <amount>] [--plot]
python ichimoku_runner.py multi       [--plot]
python ichimoku_runner.py optimize    [--pair <table>] [--metric <metric>]
python ichimoku_runner.py plot-signals [--pair <table>] [--start <idx>] [--end <idx>]
python ichimoku_runner.py plot-cloud  [--pair <table>]
```

### `config.py`

Centralized configuration for all parameters.

**Ichimoku Parameters:**

```python
ICHIMOKU_TENKAN = 9        # Conversion line period
ICHIMOKU_KIJUN = 26        # Base line period
ICHIMOKU_SENKOU_B = 52     # Cloud span B period

ATR_MULT_SL = 1.5          # Stop-loss multiplier
ATR_MULT_TP = 2.0          # Risk-reward ratio

EMA_LENGTH = 100           # Trend filter period
EMA_BACK_CANDLES = 7       # Lookback for EMA signal

ICHIMOKU_LOOKBACK = 10     # Cloud confirmation window
ICHIMOKU_MIN_CONFIRM = 5   # Min bars above/below cloud

BACKTEST_CASH = 1_000_000
BACKTEST_COMMISSION = 0.0002
```

Edit these values to adjust strategy behavior.

## Complete Workflow Example

```bash
# 1. Ensure you have data fetched
python main.py

# 2. Run backtest on one pair to inspect
python ichimoku_runner.py backtest --pair EUR_USD_daily

# 3. Run all pairs to get summary performance
python ichimoku_runner.py multi

# 4. Visualize signals for a specific time window
python ichimoku_runner.py plot-signals --pair EUR_USD_daily --start 350 --end 450

# 5. Optimize parameters for best performance
python ichimoku_runner.py optimize --pair EUR_USD_daily --metric "Return [%]"

# 6. View full Ichimoku cloud
python ichimoku_runner.py plot-cloud --pair EUR_USD_daily
```

## Programmatic Usage (Python)

You can also use the modules directly in Python scripts:

```python
from ichimoku import (
    fetch_data_from_database,
    add_ichimoku,
    add_ema_signal,
    create_ichimoku_signal,
    plot_signals_ichimoku
)
from ichimoku_backtest import run_backtest_from_database
from config import DATABASE_PATH

# Fetch and prepare data
df = fetch_data_from_database("EUR_USD_daily", DATABASE_PATH)
df = add_ichimoku(df)
df = add_ema_signal(df)
df = create_ichimoku_signal(df)

# Plot signals for rows 100-200
plot_signals_ichimoku(df, start_idx=100, end_idx=200)

# Run backtest
stats, df, bt = run_backtest_from_database("EUR_USD_daily")
print(f"Return: {stats['Return [%]']:.2f}%")
print(f"Win Rate: {stats['Win Rate [%]']:.2f}%")
```

## Configuration Tuning

To adjust strategy behavior, edit `config.py`:

### Aggressive (More Trades)
```python
ICHIMOKU_LOOKBACK = 5         # Fewer bars required
ICHIMOKU_MIN_CONFIRM = 2       # Less confirmation
ATR_MULT_SL = 1.0             # Tighter stops
ATR_MULT_TP = 3.0             # Larger targets
```

### Conservative (Fewer Trades)
```python
ICHIMOKU_LOOKBACK = 20        # More bars required
ICHIMOKU_MIN_CONFIRM = 10      # More confirmation
ATR_MULT_SL = 2.5             # Wider stops
ATR_MULT_TP = 1.5             # Smaller targets
```

### Faster Entries (Shorter EMA)
```python
EMA_LENGTH = 50               # Faster trend
EMA_BACK_CANDLES = 3          # Quicker signal
```

## Troubleshooting

**Q: "No data returned" error**
- A: Ensure you ran `python main.py` first to populate the database.

**Q: Few or no signals generated**
- A: Adjust `ICHIMOKU_LOOKBACK` and `ICHIMOKU_MIN_CONFIRM` in `config.py` to be less stringent.

**Q: Backtest shows negative returns**
- A: This is normal for any strategy on certain markets. Run `optimize` to tune parameters.

**Q: Plot shows no data**
- A: Check that `--start` and `--end` indices are within the dataframe range.

## Next Steps

1. **Refine parameters** based on your risk tolerance and market conditions
2. **Run optimization** to find best parameters for each pair
3. **Paper trade** using the signal output before real money
4. **Monitor live signals** by updating `config.py` with real-time data sources

## Files Overview

| File | Purpose |
|------|---------|
| `ichimoku.py` | Core Ichimoku calculations & plots |
| `strategy.py` | Backtesting strategy class |
| `ichimoku_backtest.py` | Orchestration & backtesting |
| `ichimoku_runner.py` | CLI interface |
| `config.py` | Centralized configuration |
| `Ichimoku.ipynb` | Original notebook (archived) |

---

**For questions or issues, refer to individual module docstrings.**
