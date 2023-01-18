import pandas as pd
import datetime
from binance.client import Client


class DataBinance:

    """Class for get historical data from Binance

    Attributes
    ----------
    ticker: str
        ticker symbol with which to work with
    start: str
        start date for data retrieval
    end: str
        end date for data retrieval

    Methods
    -------
    get_data_1hour:
        get historical data hour timeframe
    """

    def __init__(self, ticker, start, end):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.bclient = Client()

    def get_data_spot_1hour(self):
        klines = self.bclient.get_historical_klines(
            self.ticker,
            Client.KLINE_INTERVAL_1HOUR,
            self.start.strftime("%d %b %Y %H:%M:%S"),
            self.end.strftime("%d %b %Y %H:%M:%S"),
            1000,
        )
        data = pd.DataFrame(
            klines,
            columns=[
                "Date",
                "Open",
                "High",
                "Low",
                "Close",
                "Volume",
                "Close_time",
                "Quote_av",
                "Trades",
                "Tb_base_av",
                "Tb_quote_av",
                "Ignore",
            ],
        )

        data["Date"] = pd.to_datetime(data["Date"], unit="ms")
        data.set_index("Date", inplace=True)

        data = data.drop(
            ["Close_time", "Quote_av", "Trades", "Tb_base_av", "Tb_quote_av", "Ignore"],
            axis=1,
        )

        data[["Open", "High", "Low", "Close", "Volume"]] = data[
            ["Open", "High", "Low", "Close", "Volume"]
        ].apply(pd.to_numeric)
        return data


# get historical data
start_date = datetime.datetime.strptime("1 Jan 2022", "%d %b %Y")
today_date = datetime.datetime.today()
btcusdt = DataBinance("BTCUSDT", start_date, today_date)
print(btcusdt.get_data_spot_1hour())
