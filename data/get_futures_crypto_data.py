import requests
import datetime
import pandas as pd
import numpy as np


def get_binance_data_request_(
    ticker, interval="4h", limit=1500, start="2020-01-16 00:00:00"
):
    """
    interval: str tick interval - 15m/1h/4h/1d
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


btcusdt = get_binance_data_request_("BTCUSDT", "15m")
print(btcusdt)
