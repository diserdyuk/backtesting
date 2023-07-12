import pandas as pd

from calc_metrics.finance_metrics import compute_daily_returns
from read_write_data.read_write import ReadWriteData
from draw_plot.draw_chart import DrawChart
from calc_metrics.finance_metrics import FinanceMetrics


tickers = ["SPY_BA_normalize"]
path = "datafeed"
columns = ["Date", "Close_SPY", "Close_BA"]

read_data = ReadWriteData(path, tickers, columns)
df = read_data.read_data_csv()
print(df)

# compute daily returns
fin_metrics = FinanceMetrics(df)
daily_returns = fin_metrics.compute_daily_returns()
print(daily_returns)

plot = DrawChart(tickers, daily_returns, "Daily_returns", "Date", "Price", "charts")
plot.plot_data()
