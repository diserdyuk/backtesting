import yaml
import pandas as pd

from get_data.get_stock_data import GetStockData
from yaml.loader import SafeLoader
from calc_metrics.finance_metrics import log_return
from draw_plot.draw_chart import DrawChart


# read config file
with open("config.yaml", "r") as f:
    data_config = yaml.load(f, Loader=SafeLoader)

# get value 'key'
# print(data_config["key"])

"""Stocks"""

# create class instance
# stock = GetStockData("SPY", "2020-11-01", "2022-01-01")

# get data
# df = stock.get_data()
# print(df)

# chart = DrawChart("SPY", df["Close"])
# chart.draw_chart()


"""Crypto"""

# read file
df = pd.read_csv(r"datafeed/BTCUSDT_15m_2023-01-15.csv")
print(df.tail())
# print(df.iloc[-1][0])

# draw chart
chart = DrawChart("BTCUSDT", df["Close"], df, "charts")
chart.draw_chart()


"""Metrics"""
# log_return_df = log_return(df)
# print(log_return_df)


def three_bars_contra(df):

    # read cvs
    # signals in df

    pass


# draw chart
# trade logic
# metrics - winrate, profit factor
