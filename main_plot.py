import pandas as pd

from draw_plot.draw_chart import DrawChart
from read_write_data.read_write import ReadWriteData


tickers = ["BA"]
start_date = "2022-01-01"
end_date = "2023-07-01"
path = "datafeed"
columns = ["Date", "Close"]


read_data = ReadWriteData(path, tickers, columns)
df = read_data.read_data_csv()
print(df)


plot = DrawChart("BA", df, "Stock_price", "Date", "Price", "charts")
plot.plot_data()
