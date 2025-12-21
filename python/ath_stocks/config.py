"""
Configuration Module for ATH Stock Analysis System
LOCAL CSV ONLY - NO WEB DOWNLOADS
"""

import os
from datetime import datetime, timedelta

# ============================================================================
# PROJECT PATHS
# ============================================================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
CACHE_DIR = os.path.join(DATA_DIR, "ohlc_cache")
CHARTS_DIR = os.path.join(RESULTS_DIR, "charts")

# Create directories
for directory in [DATA_DIR, RESULTS_DIR, CACHE_DIR, CHARTS_DIR]:
    os.makedirs(directory, exist_ok=True)

# ============================================================================
# NIFTY 500 - LOCAL CSV ONLY (YOUR FILE REQUIRED)
# ============================================================================
NIFTY_500_LOCAL_FILE = "ind_nifty500list.csv"  # YOUR CSV FILE - REQUIRED
NIFTY_500_USE_LOCAL_ONLY = True                 # NO WEB DOWNLOADS EVER

# ============================================================================
# API & DATA SETTINGS
# ============================================================================
YFINANCE_TIMEOUT = 30
API_RATE_LIMIT_DELAY = 0.5

# ============================================================================
# ANALYSIS SETTINGS
# ============================================================================
MONTHS_OF_HISTORY = 120
LOOKBACK_DAYS = 365 * 10
BUY_PRICE_OFFSET = 1.0
WEEKLY_SMA_PERIOD = 30
WEEKLY_INTERVAL = "1wk"

# ============================================================================
# SCAN DATE
# ============================================================================
def get_current_scan_date():
    today = datetime.now()
    if (today + timedelta(days=1)).month != today.month:
        return today.date()
    else:
        last_day = (today.replace(day=1) - timedelta(days=1)).date()
        return last_day

def get_scan_date_string():
    scan_date = get_current_scan_date()
    return scan_date.strftime("%Y_%b").upper()

def get_excel_filename():
    return f"{get_scan_date_string()}.xlsx"

# ============================================================================
# LOGGING
# ============================================================================
LOG_FILE = os.path.join(RESULTS_DIR, "ath_analysis.log")
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ============================================================================
# CACHE & PERFORMANCE
# ============================================================================
CACHE_EXPIRY_DAYS = 7
BATCH_SIZE = 50
MAX_WORKERS = 5

# ============================================================================
# CHARTS
# ============================================================================
CHART_DPI = 100
CHART_FIGSIZE = (14, 7)
CHART_COLORS = {
    "ath_line": "#d62728",
    "close_price": "#1f77b4",
    "green_candle": "#2ca02c",
    "red_candle": "#d62728",
}
