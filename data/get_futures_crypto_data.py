import requests
import datetime
import pandas as pd


def get_futures_data(ticker, interval="4h", limit=1500, start="2020-01-16 00:00:00"):
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
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "qav",
        "num_trades",
        "taker_base_vol",
        "taker_quote_vol",
        "ignore",
    ]

    start = int(datetime.datetime.timestamp(pd.to_datetime(start)) * 1000)
    url = f"https://www.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&limit={limit}&startTime={start}"
    data = pd.DataFrame(requests.get(url).json(), columns=columns, dtype=float)
    data.index = [
        pd.to_datetime(x, unit="ms").strftime("%Y-%m-%d %H:%M:%S")
        for x in data.open_time
    ]

    usecols = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "qav",
        "num_trades",
        "taker_base_vol",
        "taker_quote_vol",
    ]
    data = data[usecols]
    return data


btcusdt = get_futures_data("BTCUSDT", "15m")
print(btcusdt)
