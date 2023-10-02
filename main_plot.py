import pandas as pd

from draw_plot.draw_chart import DrawChart
from read_write_data.read_write import ReadWriteData


tickers = ["BA", "AAPL"]
path = "/home/denis/backtester_files/"
columns = ["Date", "Close"]


read_data = ReadWriteData(path, tickers, columns)
df = read_data.read_data_csv()
print(df)

"""
plot = DrawChart(tickers, df, "Stock_price", "Date", "Price", "charts")
plot.plot_data()
"""
