import requests
import datetime
import pandas as pd


class GetCryptoFutData:

    """Class for get crypto data

    Attributes
    ----------
    ticker: str
        symbols of instruments
    interval:
        time frame
    interval:
        quantity of rows
    start: str
        start date for data retrieval

    Methods
    -------
    get_futures_data:
        get historical data(futures) from Binance
    """

    def __init__(self, ticker, interval, limit, start):
        self.ticker = ticker
        self.interval = interval
        self.limit = limit
        self.start = start

    def get_futures_data(self):

        """
        Function for get historical data(futures) from Binance

        Params
        ----------
        ticker: str
            ticker symbol with which to work with
        interval: str
            interval (time frame) - 15m/1h/4h/1d
        limit: int
            count rows of data feed
        start: str
            start date for data retrieval
        """

        columns = [
            "Open_time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "Close_time",
            "Qav",
            "Num_trades",
            "Taker_base_vol",
            "Taker_quote_vol",
            "Ignore",
        ]

        start = int(datetime.datetime.timestamp(pd.to_datetime(self.start)) * 1000)
        url = f"https://www.binance.com/fapi/v1/klines?symbol={self.ticker}&interval={self.interval}&limit={self.limit}&startTime={start}"
        data = pd.DataFrame(requests.get(url).json(), columns=columns, dtype=float)
        data.index = [
            pd.to_datetime(x, unit="ms").strftime("%Y-%m-%d") for x in data.Open_time
        ]

        usecols = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "Qav",
            "Num_trades",
            "Taker_base_vol",
            "Taker_quote_vol",
        ]
        data = data[usecols]
        return data
