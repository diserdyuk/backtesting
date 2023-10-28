import pandas as pd

from draw_plot.draw_chart import DrawChart
from read_write_data.read_write import ReadWriteData


tickers = ["MA"]
path = "/home/denis/backtester_files/"
columns = ["Date", "Close"]


read_data = ReadWriteData(path, tickers, columns)
df = read_data.read_data_csv()
print(df)

# plot one chart
plot = DrawChart(tickers, df, "Stock_price", "Date", "Price", path)
plot.plot_data()
