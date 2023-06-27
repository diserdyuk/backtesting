import pandas as pd

from get_data.get_stock_data import GetStockData
from yaml.loader import SafeLoader
from calc_metrics.finance_metrics import log_return
from draw_plot.draw_chart import DrawChart


# create class instance, for get 1 stokc
# stock = GetStockData(["SPY"], "2023-01-01", "2023-07-01", "datafeed")

# create class instance, for get >=2 stokcs
stock = GetStockData(["SPY"], "2023-01-01", "2023-07-01", "datafeed")

# get data
df = stock.get_data()
print(stock.ticker)
