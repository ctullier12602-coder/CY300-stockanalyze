'''
watchlist manager
'''

from typing import List, Optional
from pathlib import Path

from a_data_retriever import DataRetriever
from stock_analyzer import StockAnalyzer


class WatchlistManager:
    'Manage the stock watchlist.'
    def __init__(self, filename: str = "watchlist.txt") -> None:
        self.filename = Path(filename)
        self.watchlist: List[str] = [] # Initialize an empty watchlist to put data in.
        self.load_watchlist()

    def load_watchlist(self) -> None:
        if not self.filename.exists():
            return

        try:
            saved_tickers = self.filename.read_text().splitlines()
        except OSError:
            return

        for ticker in saved_tickers:
            self._add_stock_without_saving(ticker)

    def save_watchlist(self) -> None:
        try:
            self.filename.write_text("\n".join(self.watchlist))
        except OSError:
            pass

    def _add_stock_without_saving(self, ticker: str) -> None:
        ticker = ticker.strip().upper()
        if ticker and ticker not in self.watchlist:
            self.watchlist.append(ticker)

    def add_stock(self, ticker: str) -> None:
        ticker = ticker.strip().upper()
        if ticker and ticker not in self.watchlist: # Add a ticker to the watchlist if it's not already there.
            self.watchlist.append(ticker)
            self.save_watchlist()

    def remove_stock(self, ticker: str) -> None:
        ticker = ticker.strip().upper()
        if ticker in self.watchlist: # Remove a ticker from the watchlist.
            self.watchlist.remove(ticker)
            self.save_watchlist()

    def get_watchlist(self) -> List[str]:
        return list(self.watchlist) # Return the watchlist.

    def filter_by_volatility(
        self,
        retriever: "DataRetriever",
        analyzer: "StockAnalyzer",
        threshold: float
    ) -> List[str]:
        filtered: List[str] = [] # Initialie list to store tickers that meet volatility condition.

        for ticker in self.watchlist: # Loop through each ticker in the user's watchlist
            data = retriever.pull_data(ticker) # Pull historical data for the ticker
            if data is None or data.empty: # Skip ticker if none / df is empty
                continue

            analyzer.stock_data = data # Assign the retrieved data to the analyzer
            volatility_series = analyzer.calculate_volatility() # Calculate the rolling volatility for the ticker
            if volatility_series is  None:
                continue
               
            latest = volatility_series.dropna() # Remove NaN values
            if not latest.empty and float(latest.iloc[-1]) > threshold: # Check that the series isn't empty and latest volatility exceeds threshold
                    filtered.append(ticker)

        return filtered # Return the list that passed the volatility filter
