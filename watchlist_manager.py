import yfinance as yf
class WatchlistManager:
    def __init__(self):
        '''
        Initialize an empty watchlist to put data in.
        '''
        self.watchlist = []


    def add_stock(self, ticker): #ChatGPT, 2026. Chat defined this method. https://chatgpt.com/share/69bd37c3-fe40-8000-a9b3-52a0fdb5ca01.
        '''
        Add a ticker to the watchlist if it's not already there.
        '''
        ticker = ticker.upper()

        if ticker not in self.watchlist:
            self.watchlist.append(ticker)


    def remove_stock(self, ticker):
        '''
        Remove a ticker from the watchlist.
        '''
        if ticker in self.watchlist:
            self.watchlist.remove(ticker)


    def get_watchlist(self):
        '''
        Return the watchlist of tickers.
        '''
        return self.watchlist
    

    def filter_by_volatility(self, retriever, analyzer, threshold): #ChatGPT, 2026. created this method and explained it to me. https://chatgpt.com/share/69bd3ae9-b7e4-8000-88db-b3718895c89d
        '''
        Filter the watchlist based on volatility.
        '''
        filtered = [] # Stores tickers that pass the filter

        for ticker in self.watchlist: 
            retriever.pull_data(ticker) # Calls DataRetriever, downloads stock data, and stores in stock_data

            if retriever.stock_data is not None and not retriever.stock_data.empty: # Prevents crashes
                analyzer.stock_data = retriever.stock_data # Run the data through the analyzer
                volatility = analyzer.calculate_volatility() # Will calculate volatility from analyzer class

            if volatility is not None and volatility > threshold: 
                filtered.append(ticker) # Keeps stocks that are above threshold

        return filtered
    