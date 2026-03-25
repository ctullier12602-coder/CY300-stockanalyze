import yfinance as yf

class DataRetriever(): # ChatGPT, 2026. Created the outline for this class. https://chatgpt.com/share/69bd37c3-fe40-8000-a9b3-52a0fdb5ca01
    def __init__(self):
        '''
        Initialize an empty ticker and stock_data.
        '''
        self.ticker = None
        self.stock_data = None

    def pull_data(self, ticker):
        '''
        Download historical stock data for the given ticker.
        '''
        self.ticker = ticker.upper() 

        ticker_str = yf.Ticker(self.ticker) # https://www.geeksforgeeks.org/python/get-financial-data-from-yahoo-finance-with-python/
        self.stock_data = ticker_str.history(period= '12mo') # Grabs history
        
        print(self.stock_data.head())


    def validate_ticker(self, ticker):
        '''
        Return True if the ticker appears valid, otherwise return False.
        '''
        data = self.pull_data(ticker) # Call previous method to get data.

        if data is None or data.empty:
            print("Ticker does not exist")
            return False
        else:
            return True


    def get_current_price(self):
        '''
        Return the latest closing price from stock_data.
        '''
        if self.stock_data == None:
            return("Stock data is empty")
        elif self.stock_data.empty:
            return("Stock data is empty")
        else:
            return self.stock_data['Close'].iloc[-1] # Closing price column as pd Series, https://www.geeksforgeeks.org/python/getting-stock-data-using-yfinance-in-python/
        
