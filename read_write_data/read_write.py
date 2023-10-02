import pandas as pd
import csv


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

    """
    def read_data_csv(self):
        dataframe = pd.read_csv(
            f"{self.path}/{''.join(self.tickers)}.csv",
            index_col="Date",
            parse_dates=True,
            usecols=self.columns,
            na_values=["nan"],
        )
        return dataframe
    """

    def read_data_csv(self):
        # Open the CSV file in the root directory
        with open(self.path + self.tickers + ".csv", "r") as csv_file:
            # Create a CSV reader
            csv_reader = csv.reader(csv_file)
            # return csv_reader

            df = pd.DataFrame(csv_reader)
            df.columns = df.iloc[0]
            df = df[1:]
            df.set_index("Date", inplace=True)
            return df
