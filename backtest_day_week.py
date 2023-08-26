import pandas as pd

from read_write_data.read_write import ReadWriteData
from draw_plot.draw_chart import DrawChart
from indicators.calculate_indicator import Indicators
from calc_metrics.finance_metrics import FinanceMetrics


path_read_data = "datafeed/crypto"
path_save_data = "day_week"
ticker = "BTCUSDT"
columns = ["Date", "Open", "High", "Low", "Close", "Volume"]

data = ReadWriteData(path_read_data, ticker, columns)
df = data.read_data_csv()

# day of the week
df["Day_week"] = df.index.day_name()


result_data = []

for index, row in df.iterrows():
    if row["Day_week"] == "Monday":
        result_data.append(
            [
                index,
                row["Open"],
                row["Close"],
                # long
                row["Close"] - row["Open"],
                # Percent Change = ((New Price - Old Price) / Old Price) * 100
                ((row["Close"] - row["Open"]) / row["Open"]) * 100,
            ]
        )

# list to dataframe
df_result = pd.DataFrame(
    result_data,
    columns=[
        "Date_open",
        "Open_price",
        "Close_price",
        "Result_points",
        "Pcnt_change",
    ],
)


# cumsum
df_result["Equity_points"] = df_result["Result_points"].cumsum()
print(df_result)

df_result_plot = df_result["Equity_points"]
# df_result_plot = df_result["Pcnt_change"]
plot = DrawChart(ticker, df_result_plot, ticker, "Date", "Price", path_save_data)
plot.plot_data()
