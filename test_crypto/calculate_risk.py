import pandas as pd

from draw_plot.draw_chart import DrawChart


# read file
df_usdt = pd.read_csv(f"setup_v2_ss.csv")


def calculate_risk_pcnt(df, pcnt, account, leverage):
    """
    Calculate risk of percents,
    use XX% of account in one trade
    """

    MIN_SIZE = 0.001

    df["Result_pcnt"] = 0.0
    df["Account"] = 0.0
    df["Size"] = 0.0
    df["Result_usdt"] = 0.0

    # iterate on df
    for index, row in df.iterrows():
        # update risk account
        # 400 / 100 = 4 * 10 = 40$
        risk_usdt = (account / 100) * pcnt

        if row["Points"] < 0.0:
            # -10%
            df.at[index, "Result_pcnt"] = f"{-abs(pcnt)}"
            # 400 = 400 - 40 = 360
            account = account - risk_usdt
            df.at[index, "Account"] = account
            # 40 * -1 = -40
            df.at[index, "Result_usdt"] = risk_usdt * -1.0
        else:
            # Open_low == TP
            take_profit = row["Open_low"]
            # abs(Pcnts_25) * 16 == SL
            stop_loss = abs(row["Pcnts_25"]) * 16
            # TP / SL, 200 / 1000 = 0.2%
            result_pcnt = take_profit / stop_loss
            df.at[index, "Result_pcnt"] = result_pcnt

            # 40 * 0.2 = 8$
            df.at[index, "Result_usdt"] = risk_usdt * result_pcnt

            # 400 * 10 = 4000, 4000 / 25000 = 0.16 contracts
            max_size = (account * leverage) / row["Price_open"]
            # 40$ / 1000 pips = 0.04
            size = risk_usdt / stop_loss
            if size > max_size:
                size = max_size
            elif size < MIN_SIZE:
                size = MIN_SIZE
            # 400$ + (200 * 0.04) = 400$ + 8$ = 408
            account = account + (take_profit * size)
            df.at[index, "Account"] = account
            df.at[index, "Size"] = size
    return df


# df, pcnt, account, leverage
risk_pcnt = 20
df_res = calculate_risk_pcnt(df_usdt, risk_pcnt, 350, 20)
print(df_res)
df_res.to_csv(f"v2_ss_risk_{risk_pcnt}_pcnt.csv", index=False)

# draw chart
chart = DrawChart(
    f"BTCUSDT_v2_ss",
    df_res["Account"],
    df_res,
    "charts",
)
chart.draw_chart()
