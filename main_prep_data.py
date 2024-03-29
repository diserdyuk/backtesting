import pandas as pd

from get_data.get_stock_data import GetPrepareData


tickers = ["AAPL", "HP", "MSFT"]
start_date = "2022-01-01"
end_date = "2023-07-01"
path = "/home/denis/backtester_files/"

# create list of datetime objects
dates = pd.date_range(start_date, end_date)

# create class instance
stocks = GetPrepareData(tickers, dates, path)

multipl_df = stocks.get_data()
print(multipl_df.head())


# normalize stock prices
normalize_df = stocks.normalize_data(multipl_df)
print(normalize_df.head())
