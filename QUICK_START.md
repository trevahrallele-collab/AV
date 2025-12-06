# 🚀 Quick Start Guide - Ichimoku Integration

## ✅ Setup (One Time)

```bash
cd /workspaces/AV
source .venv/bin/activate
pip install -r requirements.txt
```

## 📊 Step 1: Fetch Data (if not done already)

```bash
python main.py
```

**Output:** Populates `forex.db` and `stocks.db` with daily data.

---

## 🎯 Step 2: Run Ichimoku Backtest

### Option A: Single Pair Test
```bash
python ichimoku_runner.py backtest --pair EUR_USD_daily
```

### Option B: All Pairs Summary
```bash
python ichimoku_runner.py multi
```

### Option C: Custom Cash & Parameters
```bash
python ichimoku_runner.py backtest --pair EUR_USD_daily --cash 500000
```

---

## 📈 Step 3: Visualize Results

### Plot Trading Signals
```bash
python ichimoku_runner.py plot-signals --pair EUR_USD_daily --start 100 --end 200
```

### Plot Full Ichimoku Cloud
```bash
python ichimoku_runner.py plot-cloud --pair EUR_USD_daily
```

---

## 🔍 Step 4: Optimize Parameters

Find best ATR & Risk-Reward multipliers:

```bash
python ichimoku_runner.py optimize --pair EUR_USD_daily
```

---

## 📚 Available Pairs (in database)

```
EUR_USD_daily    GBP_USD_daily    USD_JPY_daily
AUD_USD_daily    USD_CAD_daily
```

---

## 🎛️ Customize Strategy

Edit `config.py` to adjust:

```python
# Ichimoku Parameters
ICHIMOKU_TENKAN = 9           # Conversion line period
ICHIMOKU_KIJUN = 26           # Base line period
ICHIMOKU_SENKOU_B = 52        # Cloud span B

# Risk Management
ATR_MULT_SL = 1.5             # Stop-loss multiplier
ATR_MULT_TP = 2.0             # Risk-reward ratio

# EMA Trend Filter
EMA_LENGTH = 100              # EMA period
EMA_BACK_CANDLES = 7          # Lookback candles

# Signal Generation
ICHIMOKU_LOOKBACK = 10        # Cloud confirmation
ICHIMOKU_MIN_CONFIRM = 5      # Min bars above/below

# Backtest
BACKTEST_CASH = 1_000_000
BACKTEST_COMMISSION = 0.0002
```

---

## 📊 Example Output

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

---

## 💡 Common Tasks

| Task | Command |
|------|---------|
| Backtest EUR/USD | `python ichimoku_runner.py backtest --pair EUR_USD_daily` |
| Test all pairs | `python ichimoku_runner.py multi` |
| View signals | `python ichimoku_runner.py plot-signals --pair EUR_USD_daily --start 100 --end 200` |
| Optimize | `python ichimoku_runner.py optimize --pair EUR_USD_daily` |
| Full cloud plot | `python ichimoku_runner.py plot-cloud --pair EUR_USD_daily` |

---

## 📖 Full Documentation

- **Strategy Guide:** `ICHIMOKU_README.md`
- **Integration Details:** `INTEGRATION_SUMMARY.md`
- **Project Structure:** `PROJECT_STRUCTURE.md`
- **Data Pipeline:** `PIPELINE_README.md`

---

## 🔗 Module Quick Reference

```python
# Use directly in Python
from ichimoku_backtest import run_backtest_from_database

stats, df, bt = run_backtest_from_database("EUR_USD_daily")
print(f"Return: {stats['Return [%]']:.2f}%")
print(f"Win Rate: {stats['Win Rate [%]']:.2f}%")
```

---

## ⚡ Troubleshooting

**No data?** → Run `python main.py` first  
**Few signals?** → Lower `ICHIMOKU_MIN_CONFIRM` in config.py  
**Negative returns?** → Run `optimize` to tune parameters  
**Plot error?** → Check row indices with `--start` and `--end`  

---

**Ready to trade? Start with:**
```bash
python ichimoku_runner.py multi
```
