import pandas as pd


class ReadWriteData:

    """Class for reading data

    Attributes
    ----------
    path:
        dir for read data
    tickers: str
        symbol of instrument
    columns: list of str
        tickers

    Methods
    -------
    read_data_csv:
        read csv file and return dataframe
    """

    def __init__(self, path, tickers, columns):
        self.path = path
        self.tickers = tickers
        self.columns = columns

    def read_data_csv(self):
        dataframe = pd.read_csv(
            f"{self.path}/{''.join(self.tickers)}.csv",
            index_col="Date",
            parse_dates=True,
            usecols=["Date", "Close"],
            na_values=["nan"],
        )
        return dataframe
