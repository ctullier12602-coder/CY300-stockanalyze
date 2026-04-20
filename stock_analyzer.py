'''stock analyzer'''

from typing import List, Optional

import numpy as np
import pandas as pd

class StockAnalyzer:
    'Calculate stock indicators from price history'

    def __init__(
        self,
        stock_data: Optional[pd.DataFrame],
        rsi_period: int = 14,
        ma_window: int = 50
    ) -> None:
        """
        stock_data: pandas DataFrame from yfinance
        rsi_period: period for RSI calculation (default 14)
        ma_window: window size for moving average (default 50)
        """
        self.stock_data = stock_data
        self.rsi_period = rsi_period
        self.ma_window = ma_window

    def calculate_moving_average(self) -> Optional[pd.Series]:
        """
        Calculates simple moving average (SMA)
        Returns a pandas Series
        """
        if self.stock_data is None or len(self.stock_data) < self.ma_window:
            return None
        return self.stock_data['Close'].rolling(window=self.ma_window).mean()

    def calculate_rsi(self) -> Optional[pd.Series]:
        """
        Calculates Relative Strength Index (RSI)
        Returns a pandas Series
        """
        if self.stock_data is None or len(self.stock_data) < self.rsi_period:
            return None

        delta = self.stock_data['Close'].diff() # Calculate price changes between closing prices.
        gain = np.where(delta > 0, delta, 0) # Gains are upward movements, set others to 0
        loss = np.where(delta < 0, -delta, 0) # Losses are downward movements, set others to 0

        gain_series = pd.Series(gain, index=self.stock_data.index) # Convert gains and losses into a Series
        loss_series = pd.Series(loss, index=self.stock_data.index)

        avg_gain = gain_series.rolling(window=self.rsi_period).mean() # Calculate rolling average gain over the period for gain/loss
        avg_loss = loss_series.rolling(window=self.rsi_period).mean()

        rs = avg_gain / avg_loss # Compute relative strength (rs) as a ratio of avg gain to avg loss
        rsi = 100 - (100 / (1 + rs)) # Compute RSI using its formula

        return rsi # Return the RSI time series

    def calculate_volatility(self) -> Optional[pd.Series]:
        """
        Calculates rolling volatility (standard deviation of returns)
        Returns a pandas Series
        """
        if self.stock_data is None or len(self.stock_data) < self.ma_window:
            return None

        returns = self.stock_data['Close'].pct_change()
        volatility = returns.rolling(window=self.ma_window).std() # Calculate st. dev. of returns

        return volatility