import pandas as pd

from get_data.get_stock_data import GetStockData


tickers = ["MSFT", "BA"]
start_date = "2022-01-01"
end_date = "2023-07-01"
path = "datafeed"

# create class instance, for get 1 or more stokcs
stock = GetStockData(tickers, start_date, end_date, path)

# get data
df = stock.get_data()
print(stock.ticker)
