'''
# Crypto
# read file
df = pd.read_csv(r"datafeed/BTCUSDT_15m_2023-01-15.csv")
df["Datetime"] = pd.to_datetime(df["Datetime"])
df = df.set_index("Datetime")
df = df[["Open", "High", "Low", "Close", "Volume"]]


# Metrics
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


# Trade logic


def three_bars_contra_l(df):

    """
    0 without SL, TP XX bars
    1 create Long signal, true/false
    1.1 add avg volume per 5 prev bars
    1.2 day of week
    2 add column %-nt changed move from 1 to 3 bar
    3 hold min, time in position
    4 size, volume contracts in position
    5 iterate on dataframe
    6 save dataframe in csv format
    """

    # signal L
    df["Long"] = (
        (df["Close"] < df["Close"].shift(1))
        & (df["Close"].shift(1) < df["Close"].shift(2))
        & (df["Close"].shift(2) < df["Close"].shift(3))
        & (df["Volume"] > df["Volume"].shift(1))
        & (df["Volume"].shift(1) > df["Volume"].shift(2))
        & (df["Volume"].shift(2) > df["Volume"].shift(3))
    )

    # avg vol from 5 bars
    df["Avg_vol"] = df["Volume"] / (
        (
            df["Volume"].shift(1)
            + df["Volume"].shift(2)
            + df["Volume"].shift(3)
            + df["Volume"].shift(4)
            + df["Volume"].shift(5)
        )
        / 5
    )

    # %-nt from open 1 bar to close 3 bar
    df["Pcnt_cngd"] = (df["Open"].shift(2) - df["Close"]) / df["Open"].shift(2)

    # day of week
    df["Day_week"] = df.index.day_name()

    # trade
    HOLD_MIN = 30
    SIZE = 0.010

    result = []
    position = False

    for index, row in df.iterrows():

        if (row["Long"] == True) and (position == False):
            position = True

            # plus XX min
            new_datetime = index + pd.Timedelta(minutes=HOLD_MIN)
            date_open = index
            price_open = row["Close"]
            pcnt_cng = row["Pcnt_cngd"]
            avg_vol = row["Avg_vol"]
            day_week = row["Day_week"]

        elif position == True:
            if index == new_datetime:
                result.append(
                    [
                        date_open,
                        index,
                        price_open,
                        row["Close"],
                        row["Close"] - price_open,
                        (row["Close"] - price_open) * SIZE,
                        pcnt_cng,
                        avg_vol,
                        day_week,
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
            "Pcnt_cng",
            "Avg_vol5",
            "Day_week",
        ],
    )

    # save dataframe to csv
    df_result.to_csv(f"backtest_v1_{HOLD_MIN}m_l.csv", index=False)


def three_bars_contra_ss(df):

    """
    0 without SL, TP XX bars
    1 create SS signal, true/false
    2 add column %-nt changed move from 1 to 3 bar
    3 hold min, time in position
    4 size, volume contracts in position
    5 iterate on dataframe
    6 save dataframe in csv format
    """

    # signal SS
    df["Short"] = (
        (df["Close"] > df["Close"].shift(1))
        & (df["Close"].shift(1) > df["Close"].shift(2))
        & (df["Close"].shift(2) > df["Close"].shift(3))
        & (df["Volume"] > df["Volume"].shift(1))
        & (df["Volume"].shift(1) > df["Volume"].shift(2))
        & (df["Volume"].shift(2) > df["Volume"].shift(3))
    )

    # %-nt from open 1 bar to close 3 bar
    df["Pcnt_cngd"] = (df["Close"] - df["Open"].shift(2)) / df["Open"].shift(2)

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
            pcnt_cng = row["Pcnt_cngd"]

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
                        pcnt_cng,
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
            "Pcnt_cng",
        ],
    )

    # save dataframe to csv
    df_result.to_csv(f"backtest_v1_{HOLD_MIN}m_ss.csv", index=False)


def three_bars_contra_v2_ss(df, size):

    """
    1 with SL (above 3rd bar, High+1.0)
    2 with TP: 25%, 50%, 75%, 100%, 200%
    3 create SS signal, true/false (the same in V_1)
    4 add column %-nt changed move from 1 to 3 bar
    5 add columns 25pcnt
    6 size, volume contracts in position
    7 iterate on dataframe
    8 save dataframe in csv format
    """

    # signal SS
    df["Short"] = (
        (df["Close"] > df["Close"].shift(1))
        & (df["Close"].shift(1) > df["Close"].shift(2))
        & (df["Close"].shift(2) > df["Close"].shift(3))
        & (df["Volume"] > df["Volume"].shift(1))
        & (df["Volume"].shift(1) > df["Volume"].shift(2))
        & (df["Volume"].shift(2) > df["Volume"].shift(3))
    )

    # %-nt from open 1 bar to close 3 bar
    df["Pcnt_cngd"] = (df["Close"] - df["Open"].shift(2)) / df["Open"].shift(2)

    # part of move (from 1st to 3rd bar)
    df["25pcnt"] = (df["Close"] - df["Open"].shift(2)) / 4

    result = []
    position = False

    for index, row in df.iterrows():
        if (row["Short"] == True) and (position == False):
            position = True
            # new_datetime = index + pd.Timedelta(minutes=hold_min)
            date_open = index
            price_open = row["Close"]
            pcnt_cng = row["Pcnt_cngd"]
            pcnts_25 = row["25pcnt"]
            # SL 100%
            stop_loss = row["High"] + (abs(pcnts_25) * 4)
            take_profit = price_open - (abs(pcnts_25) * 16)

        # stop-loss
        elif (position == True) and (row["High"] >= stop_loss):
            # if index == new_datetime:
            result.append(
                [
                    date_open,
                    index,
                    price_open,
                    stop_loss,
                    price_open - stop_loss,
                    (price_open - stop_loss) * size,
                    pcnt_cng,
                    pcnts_25,
                ]
            )
            position = False

        # take-profit
        elif (position == True) and (row["Low"] < take_profit):
            result.append(
                [
                    date_open,
                    index,
                    price_open,
                    take_profit,
                    price_open - take_profit,
                    (price_open - take_profit) * size,
                    pcnt_cng,
                    pcnts_25,
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
            "Pcnt_cng",
            "Pcnts_25",
        ],
    )

    # save dataframe to csv
    df_result.to_csv("backtest_v2_ss.csv", index=False)


def three_bars_contra_v2_l(df, size, leverage_tp, leverag_sl):

    """
    1 with SL (below 3rd bar, Low-1.0)
    2 with TP: 25%, 50%, 75%, 100%, 200%
    3 create Long signal, true/false
    3.1 add avg volume per 5 prev bars
    3.2 day of week
    4 add column %-nt changed move from 1 to 3 bar
    5 add columns 25pcnt
    6 size, volume contracts in position
    7 iterate on dataframe
    8 save dataframe in csv format
    """

    # signal L
    df["Long"] = (
        (df["Close"] < df["Close"].shift(1))
        & (df["Close"].shift(1) < df["Close"].shift(2))
        & (df["Close"].shift(2) < df["Close"].shift(3))
        & (df["Volume"] > df["Volume"].shift(1))
        & (df["Volume"].shift(1) > df["Volume"].shift(2))
        & (df["Volume"].shift(2) > df["Volume"].shift(3))
    )

    # avg vol from 5 bars
    df["Avg_vol"] = df["Volume"] / (
        (
            df["Volume"].shift(1)
            + df["Volume"].shift(2)
            + df["Volume"].shift(3)
            + df["Volume"].shift(4)
            + df["Volume"].shift(5)
        )
        / 5
    )

    # %-nt from open 1 bar to close 3 bar
    df["Pcnt_cngd"] = (df["Open"].shift(2) - df["Close"]) / df["Open"].shift(2)

    # day of week
    df["Day_week"] = df.index.day_name()

    # part of move (from 1st to 3rd bar)
    df["25pcnt"] = (df["Close"] - df["Open"].shift(2)) / 4

    result = []
    position = False

    # iterate on df
    for index, row in df.iterrows():
        if (row["Long"] == True) and (position == False):
            position = True
            # new_datetime = index + pd.Timedelta(minutes=HOLD_MIN)
            date_open = index
            price_open = row["Close"]
            pcnt_cng = row["Pcnt_cngd"]
            avg_vol = row["Avg_vol"]
            day_week = row["Day_week"]
            pcnts_25 = row["25pcnt"]
            # SL, Low-1.0
            stop_loss = row["Low"] - (abs(pcnts_25) * leverag_sl)
            take_profit = price_open + (abs(pcnts_25) * leverage_tp)

        # stop-loss
        elif (position == True) and (row["Low"] <= stop_loss):
            # if index == new_datetime:
            result.append(
                [
                    date_open,
                    index,
                    price_open,
                    stop_loss,
                    stop_loss - price_open,
                    (stop_loss - price_open) * size,
                    pcnt_cng,
                    avg_vol,
                    day_week,
                    pcnts_25,
                ]
            )
            position = False

        # take-profit
        elif (position == True) and (row["High"] > take_profit):
            # if index == new_datetime:
            result.append(
                [
                    date_open,
                    index,
                    price_open,
                    take_profit,
                    take_profit - price_open,
                    (take_profit - price_open) * size,
                    pcnt_cng,
                    avg_vol,
                    day_week,
                    pcnts_25,
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
            "Pcnt_cng",
            "Avg_vol5",
            "Day_week",
            "Pcnts_25",
        ],
    )

    # save dataframe to csv
    df_result.to_csv(f"backtest_v2_l.csv", index=False)


def three_bars_contra_v2_ss(df, size, leverage_tp, leverage_sl):

    """
    1 with TP: (below 3rd bar, Low-1.0)
    2 with SL: 200-400-600%
    3 create SS signal, true/false
    3.1 add avg volume per 5 prev bars
    3.2 day of week
    4 add column %-nt changed move from 1 to 3 bar
    5 add columns 25pcnt
    6 size, volume contracts in position
    7 iterate on dataframe
    8 save dataframe in csv format
    """

    # signal L but trade in SS
    df["Long"] = (
        (df["Close"] < df["Close"].shift(1))
        & (df["Close"].shift(1) < df["Close"].shift(2))
        & (df["Close"].shift(2) < df["Close"].shift(3))
        & (df["Volume"] > df["Volume"].shift(1))
        & (df["Volume"].shift(1) > df["Volume"].shift(2))
        & (df["Volume"].shift(2) > df["Volume"].shift(3))
    )

    # avg vol from 5 bars
    df["Avg_vol"] = df["Volume"] / (
        (
            df["Volume"].shift(1)
            + df["Volume"].shift(2)
            + df["Volume"].shift(3)
            + df["Volume"].shift(4)
            + df["Volume"].shift(5)
        )
        / 5
    )

    # %-nt from open 1 bar to close 3 bar
    df["Pcnt_cngd"] = (df["Open"].shift(2) - df["Close"]) / df["Open"].shift(2)

    # day of week
    df["Day_week"] = df.index.day_name()

    # part of move (from 1st to 3rd bar)
    df["25pcnt"] = (df["Close"] - df["Open"].shift(2)) / 4

    result = []
    position = False

    # iterate on df
    for index, row in df.iterrows():
        if (row["Long"] == True) and (position == False):
            position = True
            # new_datetime = index + pd.Timedelta(minutes=HOLD_MIN)
            date_open = index
            price_open = row["Close"]
            pcnt_cng = row["Pcnt_cngd"]
            avg_vol = row["Avg_vol"]
            day_week = row["Day_week"]
            pcnts_25 = row["25pcnt"]
            price_open_low = price_open - row["Low"]
            # stop_loss = row["Low"] - (abs(pcnts_25) * leverag_sl)
            # take_profit = price_open + (abs(pcnts_25) * leverage_tp)
            take_profit = row["Low"] - 1.0
            # take_profit = row["Low"] - (abs(pcnts_25) * leverage_tp)
            # 200-400-600%
            stop_loss = price_open + (abs(pcnts_25) * leverage_sl)

        # stop-loss
        elif (position == True) and (row["High"] >= stop_loss):
            # if index == new_datetime:
            result.append(
                [
                    date_open,
                    index,
                    price_open,
                    stop_loss,
                    price_open - stop_loss,
                    (price_open - stop_loss) * size,
                    pcnt_cng,
                    avg_vol,
                    day_week,
                    pcnts_25,
                    price_open_low,
                ]
            )
            position = False

        # take-profit
        elif (position == True) and (row["Low"] < take_profit):
            # if index == new_datetime:
            result.append(
                [
                    date_open,
                    index,
                    price_open,
                    take_profit,
                    price_open - take_profit,
                    (price_open - take_profit) * size,
                    pcnt_cng,
                    avg_vol,
                    day_week,
                    pcnts_25,
                    price_open_low,
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
            "Pcnt_cng",
            "Avg_vol5",
            "Day_week",
            "Pcnts_25",
            "Open_low",
        ],
    )

    # save dataframe to csv
    df_result.to_csv(f"backtest_v2_ss.csv", index=False)


def calculate_risk_pcnt_account(df, pcnt_account, name_setup):
    """calculate risk, % of account"""
    min_size = 0.0
    max_size = 0.0

    # how add new values in row data frame?

    df["Account"] = 0.0

    df.to_csv(f"calculate_risk_{name_setup}.csv", index=False)


# three_bars_contra_v2_ss(df, 0.010)

# tp, 1==25%, 2==50%, 3==75, 4==100, 8==200, 16==400
# sl, 2==100%
# three_bars_contra_v2_l(df, 0.010, 16, 4)

# sl, 4==100, 8==200, 16==400, 24==600
three_bars_contra_v2_ss(df=df, size=0.01, leverage_tp=1, leverage_sl=16)

# three_bars_contra_ss(df)

# three_bars_contra_l(df)


# df_v2_1_ss = pd.read_csv(f"setup_v2_1_ss.csv")
# calculate_risk_pcnt_account(df_v2_1_ss, 20.0, "v_2_1_ss")


# """
# hold_min = 30
# max_cngd = 0.009
# min_cngd = 0.003
# min_avg = 2.0
# max_avg = 6.0
# days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

df_usdt = pd.read_csv(f"backtest_v2_ss.csv")

# %-cngd move 1-3 bars
# df_usdt = df_usdt[df_usdt["Pcnt_cng"] <= max_cngd]
# df_usdt = df_usdt[df_usdt["Pcnt_cng"] >= min_cngd]

# volume on 3rd bar more then 5 prev bars (1:XX)
# df_usdt = df_usdt[df_usdt["Avg_vol5"] >= min_avg]
# df_usdt = df_usdt[df_usdt["Avg_vol5"] <= max_avg]

# day of week: Mon, Tue, Wed, Thu, Sat, Sun
df_usdt = df_usdt[
    df_usdt["Day_week"].isin(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Saturday", "Sunday"]
    )
]

# day time
# to datetime format
df_usdt["Date_open"] = pd.to_datetime(df_usdt["Date_open"])
# add column with hours
df_usdt["Day_hour"] = df_usdt["Date_open"].dt.hour

# pf >= 2.0
# 1, 2, 3, 4, 6, 9, 10, 13, 14, 15, 16, 17, 18, 21, 22, 23
# >> pf >= 2.5
# 1, 2, 3, 6, 9, 10, 13, 14, 17, 21, 22, 23
# pf >= 3.0
# 1, 2, 3, 6, 9, 10, 13, 14, 17, 21, 22
# pf >= 1.5
# 1, 2, 3, 4, 6, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23

df_usdt = df_usdt[df_usdt["Day_hour"].isin([1, 2, 3, 6, 9, 10, 13, 14, 17, 21, 22, 23])]

# filter small movement
df_usdt = df_usdt[df_usdt["Open_low"] >= 50.0]

df_usdt.to_csv(f"setup_v2_ss.csv", index=False)

print(df_usdt.head(5))
print(df_usdt.tail(5))
print("")

df_usdt["Cumsum_usdt"] = df_usdt["Usdt"].cumsum()

# draw chart
chart = DrawChart(
    f"BTCUSDT_usdt_v2_ss",
    df_usdt["Cumsum_usdt"],
    df_usdt,
    "charts",
)
chart.draw_chart()

print("Result: ", df_usdt["Usdt"].sum())

wr = win_rate(df_usdt["Usdt"])
print(f"Winrate: {wr}")

pf = profit_factor(df_usdt["Usdt"])
print(f"Profit factor: {pf}")

print("Max pcnt cngd", df_usdt["Pcnt_cng"].max())
print("Min pcnt cngd", df_usdt["Pcnt_cng"].min())

avg_winnloss = avg_win_loss(df_usdt["Usdt"])
print(f"Avg winn-loss: {avg_winnloss}")

# print("Max avg", df_usdt["Avg_vol5"].max())
# print("Min avg", df_usdt["Avg_vol5"].min())

print("Trades", df_usdt["Usdt"].count())
# """
'''
