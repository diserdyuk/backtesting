import pandas as pd


# read file
df_usdt = pd.read_csv(f"setup_v2_ss.csv")


def calculate_risk_pcnt(df, pcnt, account, leverage):
    # 40$ = (400$ / 100%) * 10%
    MIN_SIZE = 0.001

    df["Result_pcnt"] = 0.0
    df["Account"] = 0.0
    df["Size"] = 0.0
    df["Result_usdt"] = 0.0

    # iterate on df
    for index, row in df.iterrows():
        if row["Points"] <= 0.0:
            # write to Result_pcnt '-{pcnt}'
            df.at[index, "Result_pcnt"] = f"{-abs(pcnt)}"

            # update_account
            risk_usdt = (account / 100) * pcnt
            account -= risk_usdt
            df.at[index, "Account"] = account
            df.at[index, "Result_usdt"] = risk_usdt * -1.0
        else:
            # Open_low == TP
            take_profit = row["Open_low"]
            # abs(Pcnts_25) * 16 == SL
            stop_loss = abs(row["Pcnts_25"]) * 16
            # TP / SL
            result_pcnt = take_profit / stop_loss
            df.at[index, "Result_pcnt"] = result_pcnt

            # update_account
            risk_usdt = (account / 100) * pcnt
            df.at[index, "Result_usdt"] = risk_usdt

            # 400 * 20 = 8000, 8000 / 25000 = 0.32 contracts
            max_size = (account * leverage) / row["Price_open"]
            # 40$ / 960pips = 0.041
            size = risk_usdt / stop_loss
            if size > max_size:
                size = max_size
            elif size < MIN_SIZE:
                size = MIN_SIZE
            account += take_profit * size
            df.at[index, "Account"] = account
            df.at[index, "Size"] = size
    return df


# calculate_risk_pcnt(df, pcnt, account, leverage)
df_res = calculate_risk_pcnt(df_usdt, 20, 350, 20)
print(df_res)
