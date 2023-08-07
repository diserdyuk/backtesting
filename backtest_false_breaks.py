import pandas as pd

from read_write_data.read_write import ReadWriteData
from draw_plot.draw_chart import DrawChart
from indicators.calculate_indicator import Indicators


path_read_data = "datafeed/crypto"
path_save_data = "false_breaks"
ticker = "BTCUSDT"
columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
# indicators
mov_avg_period = 7
rsi_period = 2
rsi_value = 30

data = ReadWriteData(path_read_data, ticker, columns)
df = data.read_data_csv()

# detect new minimum
df["Minimum"] = (df["Low"] > df["Low"].shift(1)) & (
    df["Low"].shift(1) < df["Low"].shift(2)
)
df["Min_price"] = df["Low"].shift(1)

# detect new maximum
df["Maximum"] = (df["High"] < df["High"].shift(1)) & (
    df["High"].shift(1) > df["High"].shift(2)
)
df["Max_price"] = df["High"].shift(1)
print(df.tail(10))

calc_indicators = Indicators(df)
df = calc_indicators.moving_average(mov_avg_period, "Close")
# df = calc_indicators.rsi(rsi_period, "Close")
print(df)


# iterate by df
position = False
min_price = 0.0
result_data = []
open_price = 0.0
stop_loss = 0.0
risk_divide = 1000

for index, row in df.iterrows():
    # check out SL and TP
    if position is True:
        if row["Low"] < stop_loss:
            result = stop_loss - open_price
            position = False
            result_data.append([date_open, index, open_price, stop_loss, result])
        elif row["Close"] > open_price:
            result = row["Close"] - open_price
            position = False
            result_data.append([date_open, index, open_price, row["Close"], result])

    # signal to buy
    if (row["Minimum"] is True) and (position is False):
        min_price = row["Min_price"]
    if (
        (position is False)
        and (row["Low"] < min_price)
        and (row["Close"] > min_price)
        and (row["Close"] < row["Open"])
        # and (row["RSI"] < rsi_value)
        and (row["Open"] < row["MA"])
    ):
        # open long position
        position = True
        open_price = row["Close"]
        stop_loss = row["Low"] - (row["Low"] / risk_divide)
        date_open = index

# list to dataframe
df_result = pd.DataFrame(
    result_data,
    columns=[
        "Date_open",
        "Date_close",
        "Open_price",
        "Close_price",
        "Result",
    ],
)

# save dataframe to csv
df_result["Equity"] = df_result["Result"].cumsum()
df_result.to_csv(f"{path_save_data}/backtest_false_breakrs_{ticker}.csv", index=False)
print(df_result)

df_result_plot = df_result["Equity"]
plot = DrawChart(ticker, df_result_plot, ticker, "Date", "Price", "false_breaks")
plot.plot_data()
