"""
🚀 MAIN ENTRY POINT - Run: python main.py
"""

import sys
import os  # ← ADD THIS LINE
import logging
import argparse
from datetime import datetime
from config import LOG_FILE, LOG_FORMAT, LOG_DATE_FORMAT, NIFTY_500_LOCAL_FILE, get_excel_filename
from scanner import ATHScanner


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
        handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)]
    )


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    # Verify local CSV exists
    if not os.path.exists(NIFTY_500_LOCAL_FILE):
        logger.error(f"❌ MISSING: {NIFTY_500_LOCAL_FILE}")
        logger.error("📁 Put your CSV in project folder!")
        sys.exit(1)

    logger.info("\n" + "=" * 80)
    logger.info("ATH SCANNER - LOCAL CSV + BUY/STOP LOSS")
    logger.info("=" * 80)

    try:
        scanner = ATHScanner()
        results = scanner.run_scan()

        logger.info("\n" + "=" * 80)
        logger.info("RESULTS SUMMARY")
        logger.info("=" * 80)
        logger.info(f"📊 Analyzed: {len(results['all_metrics'])}")
        logger.info(f"🎯 Selected: {len(results['selected'])}")

        if results['selected']:
            logger.info("\n🏆 TOP 5:")
            for i, stock in enumerate(results['selected'][:5], 1):
                logger.info(f"  {i}. {stock['symbol']:<10} Buy:₹{stock['buy_price']:<8} SL:₹{stock['stop_loss']}")

        logger.info(f"\n✅ EXCEL: results/{get_excel_filename()}")
        logger.info("=" * 80)

    except Exception as e:
        logger.error(f"❌ ERROR: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
