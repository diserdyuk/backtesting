import yaml
from data.get_stock_data import GetStockData
from yaml.loader import SafeLoader
from metrics.finance_metrics import log_return
from charts.draw_chart import DrawChart


# read config file
with open("config.yaml", "r") as f:
    data_config = yaml.load(f, Loader=SafeLoader)

# get value 'key'
# print(data_config["key"])


# create class instance
stock = GetStockData("SPY", "2020-11-01", "2022-01-01")

# get data
df = stock.get_data()
# print(df)

chart = DrawChart("SPY", df["Close"])
chart.draw_chart()


# log_return_df = log_return(df)
# print(log_return_df)


# draw chart
# trade logic
# metrics - winrate, profit factor
