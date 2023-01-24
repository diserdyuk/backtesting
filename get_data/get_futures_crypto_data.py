import requests
import datetime
import pandas as pd


def get_futures_crypto_data(
    ticker, interval="4h", limit=1500, start="2020-01-16 00:00:00"
):

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

    start = int(datetime.datetime.timestamp(pd.to_datetime(start)) * 1000)
    url = f"https://www.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&limit={limit}&startTime={start}"
    data = pd.DataFrame(requests.get(url).json(), columns=columns, dtype=float)
    data.index = [
        pd.to_datetime(x, unit="ms").strftime("%Y-%m-%d %H:%M:%S")
        for x in data.Open_time
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


start_date = "2020-01-01"
end_year, end_month = "2023", "01"

df = pd.DataFrame()

while True:
    # 2020 == 2023 and 01 == 01
    if start_date[0:4] == end_year and start_date[5:7] == end_month:
        df.to_csv(f"BTCUSDT_15m_{start_date}.csv")
        break
    else:
        btcusdt = get_futures_crypto_data(
            "BTCUSDT", "15m", 1500, f"{start_date} 00:00:00"
        )
        df = df.append(btcusdt)
        first_date = btcusdt.index.values[0]
        end_date = btcusdt.index.values[-1]
        print(first_date[0:10])
        print(end_date[0:10])
        print("-----------------")
        start_date = end_date[0:10]
