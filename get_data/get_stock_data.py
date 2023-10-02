import yfinance as yf
import numpy as np
import pandas as pd


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
        get one or some historical data Daily timeframe
        save data to csv format in forled
    get_info:
        get info about stock
    """

    def __init__(self, ticker, start, end, path):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.path = path
        # self.get_data()
        # self.get_info()

    def __repr__(self):
        return (
            f"GetStockData(ticker: {self.ticker}, start: {self.start}, end: {self.end})"
        )

    def get_data(self):
        for ticker in self.ticker:
            data = yf.download(ticker, self.start, self.end)
            data.index = data.index.date
            data.index = data.index.set_names("Date")
            data.rename(columns={"Adj Close": "Adj_Close"}, inplace=True)
            data.to_csv(f"{self.path}/{''.join(ticker)}.csv")
        return None

    def get_info(self):
        data = yf.Ticker(self.ticker)
        # self.stock_info = data
        return data.info


class GetPrepareData:

    """Class for prepare data, make DataFrame with some tickers

    Attributes
    ----------
    ticker: str
        symbols of instruments
    start: str
        start date for data retrieval
    end: str
        end date for data retrieval

    Methods
    -------
    get_multiple_data:
        get some tickers in Daily timeframe
        save data to csv format in forled
    get_normalize_data:
        get normalize stock data
    """

    def __init__(self, tickers, dates, path):
        self.tickers = tickers
        self.dates = dates
        self.path = path

    def get_data(self):
        """Read stock data (close) for given symbols from CSV files"""

        # create an empty dataframe with dates
        mult_df = pd.DataFrame(index=self.dates)

        # add SPY for reference, if absent
        if "SPY" not in self.tickers:
            self.tickers.insert(0, "SPY")

        for ticker in self.tickers:
            df = pd.read_csv(
                f"{self.path}{ticker}.csv",
                index_col="Date",
                parse_dates=True,
                # usecols=["Date", "Close"],
                na_values=["nan"],
            )
            # rename columns
            df = df.rename(
                columns={
                    "Open": "Open_" + ticker,
                    "High": "High_" + ticker,
                    "Low": "Low_" + ticker,
                    "Close": "Close_" + ticker,
                    "Adj_Close": "Adj_Close_" + ticker,
                    "Volume": "Volume_" + ticker,
                }
            )
            # use default how='left'
            mult_df = mult_df.join(df)

        # drop nan values
        mult_df = mult_df.dropna()
        mult_df.index = mult_df.index.set_names("Date")
        mult_df.to_csv(f"{self.path}/{'_'.join(self.tickers)}.csv")
        return mult_df

    def normalize_data(self, df):
        """normalize stock prices"""
        normalize_df = df / df.iloc[0, :]
        normalize_df.to_csv(f"{self.path}/{'_'.join(self.tickers)}_normalize.csv")
        return normalize_df
