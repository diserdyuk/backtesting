from read_write_data.read_write import ReadWriteData
from indicators.calculate_indicator import Indicators


tickers = ["MSFT"]
path = "datafeed"
columns = ["Date", "Close"]

read_data = ReadWriteData(path, tickers, columns)
df = read_data.read_data_csv()
print(df)

# compute RSI
calc_indicators = Indicators(df)
df_rsi = calc_indicators.rsi(2, "Close")
print(df_rsi.tail(10))
