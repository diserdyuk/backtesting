import pandas as pd

from read_write_data.read_write import ReadWriteData


path = "datafeed"
ticker = "BTCUSDT"
columns = ["Date", "Open", "High", "Low", "Close", "Volume"]

data = ReadWriteData(path, ticker, columns)
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


# iterate by df
position = False
min_price = 0.0

for index, row in df.iterrows():
    # signal to buy
    if (row["Minimum"] is True) and (position is False):
        min_price = row["Min_price"]
    if (
        (row["Low"] < min_price)
        and (row["Close"] > min_price)
        and (row["Close"] < row["Open"])
    ):
        print(index)
        # open position

    # check out SL and TP


"""
               Open     High      Low    Close      Volume  Minimum  Min_price  Maximum  Max_price
Date                                                                                              
2023-07-13  30368.9  31850.0  30233.0  31441.7  696023.510     True    30186.0    False    30980.5
2023-07-14  31441.6  31640.0  29876.6  30293.3  538692.246    False    30233.0     True    31850.0
2023-07-15  30293.3  30380.0  30220.2  30276.4  111622.474     True    29876.6    False    31640.0
"""
