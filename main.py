import yaml
import pandas as pd

from get_data.get_stock_data import GetStockData
from yaml.loader import SafeLoader
from calc_metrics.finance_metrics import log_return
from draw_plot.draw_chart import DrawChart


# read config file
with open("config.yaml", "r") as f:
    data_config = yaml.load(f, Loader=SafeLoader)

# get value 'key'
# print(data_config["key"])

"""Stocks"""
# create class instance
# stock = GetStockData("SPY", "2020-11-01", "2022-01-01")

# get data
# df = stock.get_data()
# print(df)


"""Crypto"""
# read file
df = pd.read_csv(r"datafeed/BTCUSDT_15m_2023-01-15.csv")
df["Datetime"] = pd.to_datetime(df["Datetime"])
df = df.set_index("Datetime")
df = df[["Open", "High", "Low", "Close", "Volume"]]


"""Metrics"""
# log_return_df = log_return(df)
# print(log_return_df)


def win_rate(value):
    total_trades = value.count()
    # print("total_trades: ", total_trades)

    win_trades = (value > 0).sum()
    # print("win trades: ", win_trades)

    win_rate = (win_trades / total_trades) * 100
    return win_rate


def profit_factor(value):
    gross_profit = (value[value > 0]).sum()
    # print("gross profit: ", gross_profit)

    gross_loss = (value[value < 0]).sum()
    # print("gross profit: ", abs(gross_loss))

    pf = gross_profit / abs(gross_loss)
    return pf


def avg_win_loss(value):
    win_trades = (value > 0).sum()
    # print(f"win trades: {win_trades}")

    gross_profit = (value[value > 0]).sum()
    # print(f"gross profit: {gross_profit}")

    avg_win = gross_profit / win_trades
    # print(f"avg winn: {avg_win}")

    total_trades = value.count()
    loss_trades = total_trades - win_trades
    # print(f"total_trades: {total_trades}, loss trades: {loss_trades}")

    gross_loss = (value[value < 0]).sum()
    # print("gross loss: ", abs(gross_loss))

    avg_loss = abs(gross_loss) / loss_trades
    # print(f"avg loss: {avg_loss}")

    return (avg_win, avg_loss)


"""Trade logic"""


def three_bars_contra(df):

    # signal
    df["Short"] = (
        (df["Close"] > df["Close"].shift(1))
        & (df["Close"].shift(1) > df["Close"].shift(2))
        & (df["Close"].shift(2) > df["Close"].shift(3))
        & (df["Volume"] > df["Volume"].shift(1))
        & (df["Volume"].shift(1) > df["Volume"].shift(2))
        & (df["Volume"].shift(2) > df["Volume"].shift(3))
    )

    # trade
    HOLD_MIN = 30
    SIZE = 0.010

    result = []
    position = False

    for index, row in df.iterrows():

        if (row["Short"] == True) and (position == False):
            position = True

            # plus XX min
            new_datetime = index + pd.Timedelta(minutes=HOLD_MIN)
            date_open = index
            price_open = row["Close"]

        elif position == True:
            # columns: date_open,date_close,price_open,price_close,points,usdt
            if index == new_datetime:
                result.append(
                    [
                        date_open,
                        index,
                        price_open,
                        row["Close"],
                        price_open - row["Close"],
                        (price_open - row["Close"]) * SIZE,
                    ]
                )
                position = False

    # list to dataframe
    df_result = pd.DataFrame(
        result,
        columns=[
            "Date_open",
            "Date_close",
            "Price_open",
            "Price_close",
            "Points",
            "Usdt",
        ],
    )

    # save dataframe to csv
    df_result.to_csv(f"backtest_v1_{HOLD_MIN}m.csv", index=False)


# three_bars_contra(df)


# """
# df_usdt = pd.read_csv("backtest_v1_30m.csv")

# test df
df_usdt = pd.DataFrame(
    data=[
        ["2020-01-01", 0.10],
        ["2020-01-02", -0.05],
        ["2020-01-03", 0.20],
        ["2020-01-04", 0.15],
        ["2020-01-05", -0.30],
        ["2020-01-06", 0.25],
        ["2020-01-07", 0.55],
        ["2020-01-08", -0.35],
        ["2020-01-09", 0.50],
        ["2020-01-10", 1.5],
        ["2020-01-11", -1.0],
        ["2020-01-12", 2.0],
        ["2020-01-13", -0.25],
        ["2020-01-14", 0.15],
        ["2020-01-15", 0.20],
    ],
    columns=["Datetime", "Usdt"],
)

# df_usdt["Cumsum_usdt"] = df_usdt["Usdt"].cumsum()
# print(df_usdt)

# draw chart
# chart = DrawChart(f"BTCUSDT_usdt_v1_30m", df_usdt["Cumsum_usdt"], df_usdt, "charts")
# chart.draw_chart()

# wr = win_rate(df_usdt["Usdt"])
# print("Winrate: ", wr)

# pf = profit_factor(df_usdt["Usdt"])
# print(pf)

# avg_winnloss = avg_win_loss(df_usdt["Usdt"])
# print(avg_winnloss)

# print("Result: ", df_usdt["Usdt"].sum())
# """
