"""
ATH Calculator with Buy Price & Stop Loss
"""

import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ATHCalculator:
    def calculate_ath_metrics(self, symbol, monthly_data, weekly_data=None):
        if monthly_data is None or monthly_data.empty:
            return None

        latest_row = monthly_data.iloc[-1]
        current_close = latest_row['Close']
        current_open = latest_row['Open']
        latest_date = monthly_data.index[-1]

        ath_value = monthly_data['Close'].max()
        ath_date = monthly_data[monthly_data['Close'] == ath_value].index[0]
        days_since_ath = (latest_date - ath_date).days

        percent_above_ath = ((current_close - ath_value) / ath_value) * 100 if ath_value > 0 else 0
        is_above_ath = current_close > ath_value
        is_green = current_close > current_open

        # BUY PRICE: Close + Rs 1
        buy_price = current_close + 1.0

        # STOP LOSS: 30-week SMA
        stop_loss = self.calculate_weekly_sma_stop_loss(weekly_data)

        return {
            'symbol': symbol,
            'company': symbol,
            'ath_value': round(ath_value, 2),
            'ath_date': ath_date.date(),
            'current_close': round(current_close, 2),
            'current_open': round(current_open, 2),
            'percent_above_ath': round(percent_above_ath, 2),
            'days_since_ath': days_since_ath,
            'is_above_ath': is_above_ath,
            'is_green': is_green,
            'latest_date': latest_date.date(),
            'buy_price': round(buy_price, 2),
            'stop_loss': round(stop_loss, 2) if stop_loss else None,
        }

    def calculate_weekly_sma_stop_loss(self, weekly_data, period=30):
        if weekly_data is None or len(weekly_data) < period:
            return None

        sma = weekly_data['Close'].rolling(window=period).mean()
        latest_sma = sma.iloc[-1]

        return float(latest_sma) if not pd.isna(latest_sma) else None

    def evaluate_selection(self, metrics):
        return metrics['is_above_ath'] and metrics['is_green'] if metrics else False

    def filter_selected_stocks(self, all_metrics):
        selected = [m for m in all_metrics if self.evaluate_selection(m)]
        selected.sort(key=lambda x: x['percent_above_ath'], reverse=True)
        return selected

    def calculate_batch_ath_no_weekly(self, symbols_data):
        """OPTIMIZATION: Calculate ATH without weekly data (faster)"""
        all_metrics = []
        total = len(symbols_data)

        for idx, (symbol, monthly_data) in enumerate(symbols_data.items(), 1):
            logger.debug(f"[{idx}/{total}] ATH only: {symbol}")
            metrics = self.calculate_ath_metrics(symbol, monthly_data, weekly_data=None)
            if metrics:
                all_metrics.append(metrics)

        return all_metrics

    def calculate_batch_ath(self, symbols_data, symbols_weekly_data):
        all_metrics = []
        total = len(symbols_data)

        for idx, (symbol, monthly_data) in enumerate(symbols_data.items(), 1):
            logger.info(f"[{idx}/{total}] Calculating: {symbol}")
            weekly_data = symbols_weekly_data.get(symbol)
            metrics = self.calculate_ath_metrics(symbol, monthly_data, weekly_data)

            if metrics:
                all_metrics.append(metrics)

        logger.info(f"✅ Calculated {len(all_metrics)} stocks")
        return all_metrics
