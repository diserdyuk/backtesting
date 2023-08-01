import pandas as pd

from get_data.get_stock_data import GetStockData
from get_data.get_crypto_futures_data import GetCryptoFutData


# Stock
"""
tickers = ["MSFT", "BA"]
start_date = "2022-01-01"
end_date = "2023-07-01"
path = "datafeed"

# create class instance, for get 1 or more stokcs
stock = GetStockData(tickers, start_date, end_date, path)

# get data
df = stock.get_data()
print(stock.ticker)
"""


# Crypto (futures)
ticker_crypto = "BTCUSDT"
time_frame = "1d"
limit_rows = 1500
start_date_crypto = "2019-01-01 00:00:00"
path = "datafeed"

crypto_fut_data = GetCryptoFutData(
    ticker_crypto, time_frame, limit_rows, start_date_crypto
)
df_btcusdt = crypto_fut_data.get_futures_data()
df_btcusdt.index.name = "Date"
print(df_btcusdt)

df_btcusdt.to_csv(f"{path}/{ticker_crypto}.csv")
