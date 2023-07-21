class Indicators:

    """Class for calculate indicators

    Attributes
    ----------
    dataframe:
        DataFrame

    Methods
    -------
    RSI
        calculate indicator RSI
    ATR (to do)
        calculate average true range
    Volatility (to do)
        calculate volatility
    """

    def __init__(self, dataframe):
        self.dataframe = dataframe

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

    def atr():
        pass

    def volatility():
        pass
