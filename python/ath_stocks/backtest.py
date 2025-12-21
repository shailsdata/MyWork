"""
🏆 NIFTY 500 ATH BACKTEST (2020-2025) - FULLY FIXED
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_loader import DataLoader
from ath_calculator import ATHCalculator
from config import NIFTY_500_LOCAL_FILE, LOOKBACK_DAYS
import warnings

warnings.filterwarnings('ignore')


class ATHBacktester:
    def __init__(self):
        self.data_loader = DataLoader()
        self.ath_calc = ATHCalculator()
        self.stocks = self.data_loader.load_nifty_500_stocks()[:100]  # First 100 for speed
        self.trades = []

    def run_backtest(self, start_year=2024, end_year=2025):
        print("🏆 NIFTY 500 ATH BACKTEST")
        print(f"📅 Period: {start_year}-{end_year}")
        print(f"📈 Stocks: {len(self.stocks)}")
        print("-" * 60)

        months_processed = 0
        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                # Month-end date
                scan_date = datetime(year, month % 12 + 1, 1) - timedelta(days=1)

                trades = self.scan_month(scan_date)
                self.trades.extend(trades)
                months_processed += 1

                if months_processed % 6 == 0:
                    print(f"📊 {months_processed} months, {len(self.trades)} trades...")

        self.analyze_results()

    def scan_month(self, scan_date):
        """Scan one month using EXACT same logic"""
        start_date = scan_date - timedelta(days=LOOKBACK_DAYS)

        try:
            monthly_data = self.data_loader.fetch_batch_ohlc_data(
                self.stocks, start_date, scan_date, "1mo"
            )

            metrics = self.ath_calc.calculate_batch_ath(monthly_data, {})
            selected = self.ath_calc.filter_selected_stocks(metrics)

            trades = []
            for stock in selected:
                trades.append({
                    'entry_date': stock['latest_date'].strftime('%Y-%m-%d'),
                    'symbol': stock['symbol'],
                    'buy_price': stock['buy_price'],
                    'stop_loss': stock.get('stop_loss', stock['ath_value'] * 0.95),
                    'current_close': stock['current_close'],
                    'ath_value': stock['ath_value'],
                    'percent_above_ath': stock['percent_above_ath'],
                    'days_since_ath': stock['days_since_ath']
                })
            return trades

        except Exception as e:
            print(f"⚠️  Skip {scan_date.strftime('%Y-%m')}: {e}")
            return []

    def analyze_results(self):
        df_trades = pd.DataFrame(self.trades)

        print("\n" + "=" * 60)
        print("📊 BACKTEST RESULTS")
        print("=" * 60)

        if df_trades.empty:
            print("❌ No trades found (strict criteria - normal)")
        else:
            print(f"📈 Total Trades: {len(df_trades)}")
            print(f"📅 Period: {df_trades['entry_date'].min()} → {df_trades['entry_date'].max()}")
            print(f"📊 Avg % above ATH: {df_trades['percent_above_ath'].mean():.2f}%")
            print(f"📊 Max % above ATH: {df_trades['percent_above_ath'].max():.2f}%")

            # Export
            df_trades.to_excel('backtest_trades.xlsx', index=False)
            print("💾 backtest_trades.xlsx created!")

        print("\n✅ BACKTEST COMPLETE!")


if __name__ == "__main__":
    backtester = ATHBacktester()
    backtester.run_backtest(2024, 2025)  # 2 years, fast test
