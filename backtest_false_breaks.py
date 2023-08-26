import pandas as pd

from read_write_data.read_write import ReadWriteData
from draw_plot.draw_chart import DrawChart
from indicators.calculate_indicator import Indicators
from calc_metrics.finance_metrics import FinanceMetrics


path_read_data = "datafeed/crypto"
path_save_data = "false_breaks"
ticker = "BTCUSDT"
columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
# indicators
mov_avg_period = 7
rsi_period = 2
rsi_value = 15

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
risk_position_usdt = 10.0
position = False
min_price = 0.0
result_data = []
open_price = 0.0
price_stop_loss = 0.0
risk_divide = 1000

for index, row in df.iterrows():
    # check out SL and TP
    if position is True:
        result_sl = price_stop_loss - open_price
        result_tp = row["Close"] - open_price

        if row["Low"] < price_stop_loss:
            result_points_sl = result_sl
            position = False
            result_data.append(
                [
                    date_open,
                    index,
                    open_price,
                    price_stop_loss,
                    result_sl,
                    result_tp,
                    result_points_sl,
                    risk_position_usdt * -1.0,
                ]
            )
        elif row["Close"] > open_price:
            result_points_tp = result_tp
            position = False
            result_data.append(
                [
                    date_open,
                    index,
                    open_price,
                    row["Close"],
                    result_sl,
                    result_tp,
                    result_points_tp,
                    abs((result_tp / result_sl)) * risk_position_usdt,
                ]
            )

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
        price_stop_loss = row["Low"] - (row["Low"] / risk_divide)
        date_open = index

# list to dataframe
df_result = pd.DataFrame(
    result_data,
    columns=[
        "Date_open",
        "Date_close",
        "Open_price",
        "Close_price",
        "Points_SL",
        "Points_TP",
        "Result_points",
        "Result_trade",
    ],
)

# save dataframe to csv
df_result["Equity_usdt"] = df_result["Result_trade"].cumsum()
df_result.to_csv(f"{path_save_data}/backtest_false_breakrs_{ticker}.csv", index=False)
print(df_result)

df_result_plot = df_result["Equity_usdt"]
plot = DrawChart(ticker, df_result_plot, ticker, "Date", "Price", "false_breaks")
plot.plot_data()

# Profit factor(PF) & WinRate
fin_metrics = FinanceMetrics(df_result["Result_trade"])
pf = fin_metrics.profit_factor()
win_rate = fin_metrics.win_rate()
print("PF:", round(pf, 2))
print("WinRate:", round(win_rate, 2))
