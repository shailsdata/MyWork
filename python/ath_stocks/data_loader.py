"""
Data Loader - LOCAL CSV ONLY + FIXED DATE HANDLING
"""

import os
import logging
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import time
from config import (
    PROJECT_ROOT, CACHE_DIR, NIFTY_500_LOCAL_FILE, NIFTY_500_USE_LOCAL_ONLY,
    YFINANCE_TIMEOUT, API_RATE_LIMIT_DELAY, LOOKBACK_DAYS, CACHE_EXPIRY_DAYS
)

logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self):
        self.cache_dir = CACHE_DIR
        os.makedirs(self.cache_dir, exist_ok=True)

    def load_nifty_500_stocks(self):
        """Load Nifty 500 from YOUR LOCAL CSV ONLY - NO WEB"""
        local_file = os.path.join(PROJECT_ROOT, NIFTY_500_LOCAL_FILE)

        if not os.path.exists(local_file):
            raise FileNotFoundError(
                f"❌ REQUIRED: {NIFTY_500_LOCAL_FILE}\n"
                f"📁 Place in: {PROJECT_ROOT}\n"
                f"💡 Columns: Company Name, Industry, Symbol"
            )

        logger.info(f"✅ Using LOCAL: {NIFTY_500_LOCAL_FILE}")
        df = pd.read_csv(local_file)

        if 'Symbol' not in df.columns:
            raise ValueError(f"❌ 'Symbol' column missing in {NIFTY_500_LOCAL_FILE}")

        symbols = df["Symbol"].str.strip().tolist()
        logger.info(f"✅ Loaded {len(symbols)} stocks")
        logger.info(f"📊 First 5: {symbols[:5]}")

        cache_file = os.path.join(self.cache_dir, "nifty_500_list.csv")
        df.to_csv(cache_file, index=False)

        return symbols

    def fetch_ohlc_data(self, symbol, start_date, end_date, interval="1mo"):
        """Fetch OHLC with FIXED date comparison"""
        cache_file = os.path.join(self.cache_dir, f"{symbol}_{interval}.csv")

        if os.path.exists(cache_file):
            cached_data = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            if len(cached_data) > 0:
                # FIXED: Convert both to date for comparison
                cache_date = cached_data.index[-1].date()
                end_date_fixed = pd.to_datetime(end_date).date()
                if cache_date >= end_date_fixed:
                    logger.debug(f"✅ Cache hit: {symbol}")
                    return cached_data

        try:
            logger.debug(f"📥 {interval}: {symbol}")
            ticker = yf.Ticker(f"{symbol}.NS")
            data = ticker.history(start=start_date, end=end_date, interval=interval)

            if data.empty:
                logger.warning(f"❌ No data: {symbol}")
                return None

            data.to_csv(cache_file)
            return data

        except Exception as e:
            logger.error(f"❌ Error {symbol}: {e}")
            return None

    def fetch_batch_ohlc_data(self, symbols, start_date, end_date, interval="1mo"):
        """Batch fetch with rate limiting"""
        results = {}
        total = len(symbols)

        for idx, symbol in enumerate(symbols, 1):
            logger.info(f"[{idx}/{total}] {symbol}...")
            data = self.fetch_ohlc_data(symbol, start_date, end_date, interval)

            if data is not None:
                results[symbol] = data

            time.sleep(API_RATE_LIMIT_DELAY)

        logger.info(f"✅ Fetched {len(results)}/{total} stocks")
        return results
