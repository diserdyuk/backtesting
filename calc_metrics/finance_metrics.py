import numpy as np


def profit_factor():
    pass


def win_rate():
    pass


def max_dd():
    pass


def max_loss_in_posit():
    pass


def sharp():
    pass


def correlation():
    pass


class FinanceMetrics:

    """Class for calculate finance and statistics metrics

    Attributes
    ----------
    dataframe:
        DataFrame

    Methods
    -------
    compute_daily_returns:
        compute and return the daily return values
    log_returns
        calculate log return (np.log) on base Close price
    """

    def __init__(self, dataframe):
        self.dataframe = dataframe

    def compute_daily_returns(self):
        """Compute and return the daily return values"""
        dr_dataframe = (self.dataframe / self.dataframe.shift(1)) - 1
        dr_dataframe.iloc[0] = 0
        return dr_dataframe

    def log_return(self):

        """
        Calculate log return (np.log) on base Close price

        Params
        ----------
        data: DataFrame
            using column 'Close' price
        """

        self.dataframe["Log_return"] = np.log(
            self.dataframe.Close / self.dataframe.Close.shift(1)
        )
        return self.dataframe

    # TEST
    def rsi(self, window_length):

        """
        Calculate RSI


        Params
        ----------
        data: DataFrame
            using column 'Data' and 'Close' price
        window_lengts:
            period of RSI
        """

        # calculate Price Differences
        self.dataframe["price_diff"] = self.dataframe.diff(1)

        # calculate Avg.Gains/Losses
        self.dataframe["gain"] = self.dataframe["price_diff"].clip(lower=0).round(2)
        self.dataframe["loss"] = (
            self.dataframe["price_diff"].clip(upper=0).abs().round(2)
        )

        # get initial averages
        self.dataframe["avg_gain"] = (
            self.dataframe["gain"]
            .rolling(window=window_length, min_periods=window_length)
            .mean()[: window_length + 1]
        )
        self.dataframe["avg_loss"] = (
            self.dataframe["loss"]
            .rolling(window=window_length, min_periods=window_length)
            .mean()[: window_length + 1]
        )

        # get WMS averages
        # average gains
        for i, row in enumerate(self.dataframe["avg_gain"].iloc[window_length + 1 :]):
            self.dataframe["avg_gain"].iloc[i + window_length + 1] = (
                self.dataframe["avg_gain"].iloc[i + window_length] * (window_length - 1)
                + self.dataframe["gain"].iloc[i + window_length + 1]
            ) / window_length

        # average losses
        for i, row in enumerate(self.dataframe["avg_loss"].iloc[window_length + 1 :]):
            self.dataframe["avg_loss"].iloc[i + window_length + 1] = (
                self.dataframe["avg_loss"].iloc[i + window_length] * (window_length - 1)
                + self.dataframe["loss"].iloc[i + window_length + 1]
            ) / window_length

        # calculate RS values
        self.dataframe["rs"] = self.dataframe["avg_gain"] / self.dataframe["avg_loss"]

        # calculate RSI
        self.dataframe["rsi"] = 100 - (100 / (1.0 + self.dataframe["rs"]))

        # print(df.tail(40))
        return self.dataframe
