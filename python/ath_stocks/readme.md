# ⚡ QUICK START GUIDE

## 🎯 Objective
Identify Nifty 500 stocks breaking ATH with calculated buy prices and stop losses, exported to Excel.

---

## 🚀 3-Minute Setup

### 1️⃣ Install (30 seconds)
```bash
pip install -r requirements.txt
```

### 2️⃣ Run (5-10 minutes on first run)
```bash
python main.py
```

### 3️⃣ Results (Check Excel)
```
results/2025_DEC.xlsx  (or current month)
```

**Done!** ✅

---

## 📊 Excel Output

| Column | What It Is |
|--------|-----------|
| stock_name | Stock symbol |
| stock_symbol | Ticker (e.g., RELIANCE) |
| **buy_price** | Close + Rs 1.00 ← Entry price |
| **stop_loss** | 30-week SMA ← Exit price |
| current_close | Latest close |
| ath_value | All-time high |
| percent_above_ath | % above ATH |

---

## 📈 How It Works

### Step 1: Load Stocks
Downloads list of 500 Nifty stocks

### Step 2: Fetch Data
Gets 10 years of monthly & weekly data

### Step 3: Calculate Metrics
- ATH (all-time high)
- Buy Price = Close + Rs 1
- Stop Loss = 30-week SMA

### Step 4: Filter Stocks
Selects only:
1. Stocks above ATH
2. With green monthly candles

### Step 5: Export Excel
Creates: `2025_DEC.xlsx` with all data

---

## 💰 Example Results

**RELIANCE**
- Current Close: Rs 2,880
- Buy Price: Rs 2,881 (close + 1)
- Stop Loss: Rs 2,750 (30-week SMA)
- Selection: ✅ SELECTED

---

## ⏱️ How Long It Takes

| First Run | Next Runs |
|-----------|-----------|
| 5-10 min | <1 min |
| (Downloads all data) | (Uses cache) |

---

## 🛠️ Different Run Options

**Normal (Full Features)**
```bash
python main.py
```

**Fast (No Charts)**
```bash
python main.py --no-charts
```

**Fresh Data (No Cache)**
```bash
python main.py --no-cache
```

**Debug (Verbose Logs)**
```bash
python main.py --debug
```

---

## 📁 File Structure

```
project/
├── config.py              ← Configuration
├── data_loader.py         ← Download data
├── ath_calculator.py      ← Calculate metrics
├── scanner.py             ← Main orchestrator
├── visualizer.py          ← Charts
├── main.py                ← Run this
├── requirements.txt       ← Install these
└── results/
    └── 2025_DEC.xlsx  ✅ YOUR OUTPUT
```

---

## ❓ FAQ

**Q: How long does it take?**
A: First time 5-10 min (downloads), then <1 min (cached)

**Q: What's in the Excel?**
A: stock_name, symbol, buy_price, stop_loss, ATH value, etc.

**Q: How often should I run it?**
A: Once per month (month-end) or anytime for current state

**Q: What if some data is missing?**
A: Normal - some very new stocks may not have enough history

**Q: Can I customize buy price or SMA?**
A: Yes! Edit in `config.py` and `ath_calculator.py`

---

## 🎯 Selection Criteria

Stock is selected if BOTH are true:
1. ✅ Current close > ATH
2. ✅ Green monthly candle (close > open)

---

## 🚨 Troubleshooting

**Error: ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**No results?**
- Normal if few stocks break ATH this month
- Check log file: `results/ath_analysis.log`

**Slow first run?**
- Normal! Downloads 500 stocks × 100+ months
- Next runs are super fast (<1 min)

**API rate limit?**
- Wait 5 minutes
- Or use cache: remove `--no-cache` flag

---

## 📊 Understanding the Output

### Excel File: 2025_DEC.xlsx

**buy_price** = How much to pay (entering trade)
- Formula: Closing Price + Rs 1.00
- Example: Close Rs 2,500 → Buy at Rs 2,501

**stop_loss** = Where to exit if wrong (risk management)
- Formula: 30-week SMA on weekly chart
- Example: SMA Rs 2,400 → Stop loss at Rs 2,400

**Profit/Loss Example:**
- Entry (buy_price): Rs 2,501
- Exit if loss (stop_loss): Rs 2,400
- Risk per share: Rs 101 loss max

---

## ✨ Key Features

✅ Automated monthly scans
✅ Professional Excel export (YYYY_MMM.xlsx)
✅ Auto-calculated buy prices
✅ Auto-calculated stop losses
✅ Smart caching (fast subsequent runs)
✅ Detailed logging (results/ath_analysis.log)
✅ Error handling & recovery
✅ Production-ready code

---

## 🎉 Let's Get Started!

```bash
# Copy and paste:
pip install -r requirements.txt
python main.py

# Check results:
ls results/
```

Your Excel file will be ready in 10 minutes!

---

## 📞 Next Steps

Once you have the Excel file:
1. Review the selected stocks
2. Check buy prices and stop losses
3. Decide which stocks to trade
4. Ready to automate more? Ask for Phase 2!

---

**Status:** ✅ Ready to Use
**Last Updated:** December 21, 2025
