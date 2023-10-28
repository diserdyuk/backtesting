from read_write_data.read_write import ReadWriteData
from draw_plot.draw_chart import DrawChart
from calc_metrics.finance_metrics import FinanceMetrics


path = "/home/denis/backtester_files/"
tickers = ["MSFT"]
columns = ["Date", "Close"]

read_data = ReadWriteData(path, tickers, columns)
df = read_data.read_data_csv()
print(df)

# compute daily returns
fin_metrics = FinanceMetrics(df)
daily_returns = fin_metrics.daily_returns()
print(daily_returns)

plot = DrawChart(tickers, daily_returns, "Daily_returns", "Date", "Price", path)
plot.plot_data()
