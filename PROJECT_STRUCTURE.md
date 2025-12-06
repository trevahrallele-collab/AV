# Project Structure

## 📁 Directory Overview

```
/workspaces/AV/
│
├── 🔷 Data & Databases
│   ├── forex.db                    # SQLite database with forex daily data
│   ├── stocks.db                   # SQLite database with stock data
│   └── *.csv                       # CSV exports of all data
│
├── 🟦 Core Data Pipeline
│   ├── config.py                   # Central configuration (API, DB paths, params)
│   ├── data_fetcher.py             # Alpha Vantage API data fetching
│   ├── database.py                 # SQLite save/load operations
│   ├── main.py                     # Data fetching orchestration
│   ├── plot_main.py                # Chart generation pipeline
│   └── plotting.py                 # Plotly visualization functions
│
├── 🟩 Ichimoku Trading Strategy
│   ├── ichimoku.py                 # Core Ichimoku indicators & signals (17 KB)
│   ├── strategy.py                 # SignalStrategy for backtesting (2 KB)
│   ├── ichimoku_backtest.py        # Backtest orchestration (9 KB)
│   ├── ichimoku_runner.py          # CLI interface (5 KB)
│   └── run_ichimoku.py             # Quick start entry point
│
├── 📚 Documentation
│   ├── README.md                   # Original project README
│   ├── PIPELINE_README.md          # Data pipeline documentation
│   ├── ICHIMOKU_README.md          # Ichimoku strategy guide (13 KB)
│   ├── INTEGRATION_SUMMARY.md      # Integration overview (6.5 KB)
│   └── PROJECT_STRUCTURE.md        # This file
│
├── 📓 Notebooks
│   ├── building.ipynb              # Original data pipeline notebook
│   └── Ichimoku.ipynb              # Original Ichimoku notebook
│
├── 📦 Configuration
│   ├── requirements.txt             # Python dependencies
│   └── .venv/                       # Virtual environment
│
└── 📊 Generated Outputs
    ├── EUR_USD_daily.html          # Candlestick chart
    ├── GBP_USD_daily.html          # Candlestick chart
    ├── USD_JPY_daily.html          # Candlestick chart
    ├── AUD_USD_daily.html          # Candlestick chart
    ├── USD_CAD_daily.html          # Candlestick chart
    └── (CSV files for each symbol)
```

## 📋 Module Dependency Graph

```
┌─────────────────────────────────────────────────────────────────┐
│                         config.py                               │
│      (Central configuration, all modules import from here)      │
└──────────────────────┬──────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ↓              ↓              ↓
    data_fetcher   database.py    plotting.py
    (yfinance)     (SQLAlchemy)    (Plotly)
        │              │              │
        └──────────────┼──────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ↓                             ↓
    main.py                      plot_main.py
(Data pipeline)              (Visualization)
        │                             │
        └─────────────┬───────────────┘
                      │
                   forex.db ←── ichimoku.py
                   stocks.db     (reads from DB)
                      │              │
                      └──────────┬───┘
                                 │
                                 ↓
                       ┌─────────────────────┐
                       │  add_ichimoku()     │
                       │  add_ema_signal()   │
                       │  create_signal()    │
                       │  plot_*()           │
                       └─────────────────────┘
                                 │
                                 ↓
                           strategy.py
                        (SignalStrategy)
                                 │
                                 ↓
                      ichimoku_backtest.py
               (Orchestration + Backtesting)
                                 │
                                 ↓
                       ichimoku_runner.py
                          (CLI Interface)
```

## 🚀 Usage Paths

### Path 1: Data Pipeline Only
```
main.py → forex.db, stocks.db → CSV exports
```

### Path 2: Visualization Only
```
forex.db → plot_main.py → HTML charts
```

### Path 3: Ichimoku Strategy (Complete)
```
forex.db → ichimoku.py → ichimoku_backtest.py → Results
                      ↓
                ichimoku_runner.py (CLI)
```

## 📝 File Purposes

| File | Purpose | Size | Depends On |
|------|---------|------|-----------|
| config.py | Centralized settings | 2.6K | os |
| data_fetcher.py | API data fetching | 3.3K | requests, yfinance |
| database.py | DB operations | 2.5K | sqlalchemy, pandas |
| plotting.py | Chart functions | 4.7K | plotly, pandas |
| main.py | Data pipeline | 3.8K | data_fetcher, database |
| plot_main.py | Visualization | 4.7K | database, plotting |
| **ichimoku.py** | **Ichimoku indicators** | **17K** | **pandas_ta, database** |
| **strategy.py** | **Backtest strategy** | **2.1K** | **backtesting** |
| **ichimoku_backtest.py** | **Orchestration** | **8.6K** | **ichimoku, strategy** |
| **ichimoku_runner.py** | **CLI interface** | **5.2K** | **ichimoku_backtest** |
| run_ichimoku.py | Entry point | 358B | ichimoku_runner |

## 🔄 Data Flow Example

```
Step 1: Fetch Data
──────────────────
$ python main.py
  → Fetches AAPL, EUR/USD, GBP/USD, USD/JPY, AUD/USD, USD/CAD
  → Saves to forex.db, stocks.db
  → Exports CSVs

Step 2: Run Ichimoku Backtest
──────────────────────────────
$ python ichimoku_runner.py backtest --pair EUR_USD_daily
  → ichimoku.py: fetch_data_from_database("EUR_USD_daily")
  → ichimoku.py: add_ichimoku() [Tenkan, Kijun, Span A/B, ATR]
  → ichimoku.py: add_ema_signal() [EMA trend filter]
  → ichimoku.py: create_ichimoku_signal() [Trading signals]
  → strategy.py: SignalStrategy [Entry/Exit logic]
  → ichimoku_backtest.py: run_backtest() [Execute backtest]
  → Output: Return %, Max DD, Win Rate, # Trades

Step 3: Visualize Results
──────────────────────────
$ python ichimoku_runner.py plot-signals --pair EUR_USD_daily --start 100 --end 200
  → ichimoku.py: fetch_data_from_database()
  → ichimoku.py: add_ichimoku()
  → ichimoku.py: add_ema_signal()
  → ichimoku.py: create_ichimoku_signal()
  → ichimoku.py: plot_signals_ichimoku() [Interactive Plotly]
  → Display chart with candles, cloud, EMA, signals
```

## 🔧 Configuration Hierarchy

```
1. Default values in config.py
   ↓
2. Environment variables (e.g., ALPHA_VANTAGE_API_KEY)
   ↓
3. Command-line arguments (in ichimoku_runner.py)
   ↓
4. Function parameters
```

Example:
```python
# In config.py (default)
ICHIMOKU_TENKAN = 9

# Can override with environment variable
export ICHIMOKU_TENKAN=12  # (not currently supported, but easy to add)

# Or in code
from ichimoku_backtest import run_backtest_from_database
run_backtest_from_database(..., tenkan=12)
```

## 📊 Database Schema

### forex.db
```sql
CREATE TABLE EUR_USD_daily (
    index DATETIME,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume INT
)

-- Same structure for:
-- GBP_USD_daily, USD_JPY_daily, AUD_USD_daily, USD_CAD_daily
```

### stocks.db
```sql
CREATE TABLE AAPL_daily (
    index DATETIME,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    volume INT
)
```

## 🎯 Key Classes & Functions

### ichimoku.py
- `add_ichimoku()` - Add Ichimoku indicators to DataFrame
- `add_ema_signal()` - Add EMA trend filter
- `create_ichimoku_signal()` - Generate trading signals
- `plot_signals_ichimoku()` - Visualize signals on candles
- `plot_ichimoku_cloud()` - Full Ichimoku analysis plot

### strategy.py
- `SignalStrategy` - Backtesting strategy class
  - `init()` - Initialize strategy
  - `next()` - Execute per-bar logic

### ichimoku_backtest.py
- `run_backtest_from_database()` - Single pair backtest
- `run_all_pairs_backtest()` - Multi-pair summary
- `optimize_strategy()` - Grid search parameter tuning

### ichimoku_runner.py
- `main()` - CLI entry point with subcommands
  - `backtest` - Single pair test
  - `multi` - All pairs test
  - `optimize` - Parameter optimization
  - `plot-signals` - Signal visualization
  - `plot-cloud` - Full Ichimoku plot

## �� Testing

Run individual components:

```bash
# Test data pipeline
python main.py

# Test Ichimoku calculations
python - <<'PY'
from ichimoku import fetch_data_from_database, add_ichimoku
df = fetch_data_from_database("EUR_USD_daily")
df = add_ichimoku(df)
print(df[["Close", "ich_tenkan", "ich_kijun", "ich_spanA", "ich_spanB"]].tail())
PY

# Test backtest
python ichimoku_runner.py backtest --pair EUR_USD_daily

# Test multi-pair
python ichimoku_runner.py multi
```

## 📈 Output Examples

### Backtest Results
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

### Multi-Pair Summary
```
       Pair  Return [%]  Max DD [%]  Avg DD [%]  Win Rate [%]  # Trades  Exposure [%]
0  EUR/USD      -75.43      -87.67      -15.23          35.06         77         20.23
1  GBP/USD      -97.66      -97.84      -18.50          28.00         75         19.20
2  USD/JPY      -86.85      -96.64      -17.85          33.33         87         22.02
3  AUD/USD      -98.22      -99.73      -20.10          32.86         70         22.77
4  USD/CAD      -73.86      -88.43      -16.30          38.46         78         24.53
   AVERAGE      -86.40      -94.06      -17.76          33.54         77         21.75
```

---

**For detailed documentation, see:**
- `ICHIMOKU_README.md` - Strategy and usage guide
- `PIPELINE_README.md` - Data pipeline documentation
- `INTEGRATION_SUMMARY.md` - Integration overview
