import numpy as np


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
    profit_factor (to do)
        calculate profit factor
    win_rate (to do)
        calculate win rate
    max_dd (to do)
        calculate max draw down
    max_loss_in_posit (to do)
        calculate max draw down when was opening position
    sharp (to do)
        calculate sharp
    correlation (to do)
        calculation correlation
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
