'''data retriever'''

from typing import List, Optional

import pandas as pd
import yfinance as yf

class DataRetriever:
    'Download and validate the stock data.'

    def __init__(self) -> None: # Initialize an empty ticker and stock_data.
        self.ticker: Optional[str] = None
        self.stock_data: Optional[pd.DataFrame] = None

    def pull_data(self, ticker: str) -> Optional[pd.DataFrame]: # Download historical stock data for the given ticker.
        self.ticker = ticker.strip().upper()
        if not self.ticker: # If ticker is not valid:
            self.stock_data = None
            return None
        try: # Call yfinance.Ticker to get the history
            ticker_obj = yf.Ticker(self.ticker)
            data = ticker_obj.history(period= '12mo')
        except Exception: # Handle exceptions
            self.stock_data = None
            return None
       
        self.stock_data = data
        return data

    def validate_ticker(self, ticker: str) -> bool: # Return True if the ticker appears valid, otherwise return False.
        data = self.pull_data(ticker)
        if data is None or data.empty: # Validate condition
            return False
        return True

    def get_current_price(self) -> Optional[float]: # Return the latest closing price from stock_data.
        if self.stock_data is None or self.stock_data.empty:
            return None
        return float(self.stock_data['Close'].iloc[-1]) # Locate the closing stock position in the -1 index.
