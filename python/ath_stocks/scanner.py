"""
Main Scanner - OPTIMIZED: Weekly data ONLY for selected stocks
"""

import os
import json
import pandas as pd
import logging
from datetime import timedelta
from data_loader import DataLoader
from ath_calculator import ATHCalculator
from config import (
    RESULTS_DIR, LOOKBACK_DAYS, get_current_scan_date, get_excel_filename,
    get_scan_date_string
)

logger = logging.getLogger(__name__)


class ATHScanner:
    def __init__(self):
        self.data_loader = DataLoader()
        self.ath_calculator = ATHCalculator()
        self.scan_date = get_current_scan_date()

    def run_scan(self):
        logger.info("=" * 80)
        logger.info(f"🚀 OPTIMIZED ATH Scan: {self.scan_date}")
        logger.info("💡 Weekly data ONLY for selected stocks")
        logger.info("=" * 80)

        # 1. Load stocks (YOUR LOCAL CSV)
        stocks = self.data_loader.load_nifty_500_stocks()

        # 2. Monthly data (ALL stocks)
        start_date = self.scan_date - timedelta(days=LOOKBACK_DAYS)
        logger.info("\n📊 Step 1: Monthly data (ALL stocks)...")
        monthly_data = self.data_loader.fetch_batch_ohlc_data(stocks, start_date, self.scan_date, "1mo")

        # 3. Calculate ATH + Green filter FIRST
        logger.info("\n🔢 Step 2: ATH + Green filter...")
        metrics = self.ath_calculator.calculate_batch_ath(monthly_data, {})
        selected_stocks = self.ath_calculator.filter_selected_stocks(metrics)
        logger.info(f"🎯 Selected: {len(selected_stocks)} stocks")

        # 4. ONLY fetch weekly for selected stocks
        if selected_stocks:
            symbols = [stock['symbol'] for stock in selected_stocks]
            logger.info(f"\n⏱️  Step 3: Weekly data ({len(symbols)} selected stocks)...")
            weekly_data = self.data_loader.fetch_batch_ohlc_data(symbols, start_date, self.scan_date, "1wk")

            # Recalculate with stop loss
            logger.info("💰 Step 4: Stop loss calculation...")
            final_metrics = self.ath_calculator.calculate_batch_ath(monthly_data, weekly_data)
            selected_stocks = self.ath_calculator.filter_selected_stocks(final_metrics)
        else:
            logger.info("⚠️  No selected stocks - skipping weekly data")

        # 5. Export
        logger.info("\n💾 Step 5: Exporting...")
        self.export_results(selected_stocks, metrics)

        logger.info("=" * 80)
        logger.info(f"✅ COMPLETE! {len(selected_stocks)} stocks → {get_excel_filename()}")
        logger.info("=" * 80)

        return {'selected': selected_stocks, 'all_metrics': metrics, 'scan_date': self.scan_date}

    def export_results(self, selected_stocks, all_metrics):
        scan_date_str = get_scan_date_string()

        # Excel (MAIN OUTPUT)
        if selected_stocks:
            self.export_to_excel(selected_stocks)
        else:
            logger.warning("⚠️  No selected stocks - empty Excel created")
            pd.DataFrame(columns=['stock_name', 'stock_symbol', 'buy_price', 'stop_loss']).to_excel(
                os.path.join(RESULTS_DIR, get_excel_filename()), index=False
            )

        # Full analysis CSV
        if all_metrics:
            df_all = pd.DataFrame(all_metrics)
            csv_file = os.path.join(RESULTS_DIR, f"ath_scan_full_{scan_date_str}.csv")
            df_all.to_csv(csv_file, index=False)
            logger.info(f"📄 Full analysis: {csv_file} ({len(df_all)} stocks)")

        # Summary JSON
        summary = {
            'scan_date': str(self.scan_date),
            'total_analyzed': len(all_metrics),
            'ath_crossing': len([m for m in all_metrics if m['is_above_ath']]),
            'green_candles': len([m for m in all_metrics if m['is_green']]),
            'selected': len(selected_stocks),
            'selection_rate': round(len(selected_stocks) / len(all_metrics) * 100, 2) if all_metrics else 0
        }
        json_file = os.path.join(RESULTS_DIR, f"ath_scan_summary_{scan_date_str}.json")
        with open(json_file, 'w') as f:
            json.dump(summary, f, indent=2)
        logger.info(f"📊 Summary: {json_file}")

    def export_to_excel(self, selected_stocks):
        """Create YYYY_MMM.xlsx"""
        excel_data = [{
            'stock_name': stock['company'],
            'stock_symbol': stock['symbol'],
            'buy_price': stock['buy_price'],
            'stop_loss': stock.get('stop_loss', 'N/A'),
            'current_close': stock['current_close'],
            'ath_value': stock['ath_value'],
            'percent_above_ath': stock['percent_above_ath'],
            'days_since_ath': stock['days_since_ath']
        } for stock in selected_stocks]

        df = pd.DataFrame(excel_data)
        excel_file = os.path.join(RESULTS_DIR, get_excel_filename())
        df.to_excel(excel_file, index=False, sheet_name='ATH_Selection')
        logger.info(f"✅ EXCEL: {excel_file} ({len(df)} stocks)")
