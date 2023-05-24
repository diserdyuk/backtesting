import pandas as pd


# read file
df_usdt = pd.read_csv(f"setup_v2_ss.csv")


for index, row in df_usdt.iterrows():
    print(index)


def calculate_risk_pcnt(df, pcnt, account, leverage):
    # Open_low == TP
    # abs(Pcnts_25) * 16 == SL
    # TP / SL
    # if Points == "-" -> -1%

    # 4000$ = 400$ * 10lev
    BP = account * leverage
    # 40$ = 400$ / 100% * 10%
    RISK_USDT = (account / 100) * pcnt
    MIN_SIZE = 0.001

    # iterate on df
    for index, row in df.iterrows():
        # if
        print(row["Price_open"])


# calculate_risk_pcnt(df, pcnt, account, leverage)
calculate_risk_pcnt(df_usdt, 10, 400, 10)
