import pandas as pd

from get_data.get_stock_data import GetStockData


# stock
tickers = ["MSFT", "GILD"]
start_date = "2022-01-01"
end_date = "2023-01-01"

# save files on local disk
path = "/home/denis/backtester_files/"

# create class instance, for get 1 or more stokcs
stock = GetStockData(tickers, start_date, end_date, path)

# get data
df = stock.get_data()
print(stock.ticker)
