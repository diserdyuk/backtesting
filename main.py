import yaml
from data.get_stock_data import GetStockData
from yaml.loader import SafeLoader


# read config file
with open("config.yaml", "r") as f:
    data_config = yaml.load(f, Loader=SafeLoader)

# get value 'key'
# print(data_config["key"])


# create class instance
stock = GetStockData("DIS", "2020-11-01", "2022-01-01")

# get attribute class
print(stock.ticker)

# get data
dis_df = stock.get_data()
print(dis_df)
