import yfinance as yf
import numpy as np


class GetStockData:

    """Class for get historical data from Yahoo finance

    Attributes
    ----------
    ticker: str
        symbol of instrument
    start: str
        start date for data retrieval
    end: str
        end date for data retrieval

    Methods
    -------
    repr:
        get info about params class
    get_data:
        get historical data Daily timeframe
    get_info:
        get info about stock
    """

    def __init__(self, ticker, start, end):
        self.ticker = ticker
        self.start = start
        self.end = end
        # self.get_data()
        # self.get_info()

    def __repr__(self):
        return (
            f"GetStockData(ticker: {self.ticker}, start: {self.start}, end: {self.end})"
        )

    def get_data(self):
        data = yf.download(self.ticker, self.start, self.end)
        # self.data = data
        return data

    def get_info(self):
        data = yf.Ticker(self.ticker)
        # self.stock_info = data
        return data.info


# stock = GetStockData("SPY", "2020-10-01", "2020-11-01")

# get attribute, ticker
# print(stock.ticker)
# print(stock.start, stock.end)

# df = stock.get_data()
# print(df)

# print(stock.get_info())
