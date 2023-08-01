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

    def daily_returns(self):

        """Compute and return the daily return values"""

        dr_dataframe = (self.dataframe / self.dataframe.shift(1)) - 1
        dr_dataframe.iloc[0] = 0
        return dr_dataframe

    def log_return(self):

        """Calculate log return (np.log) on base Close price"""

        self.dataframe["Log_return"] = np.log(
            self.dataframe.Close / self.dataframe.Close.shift(1)
        )
        return self.dataframe

    def win_rate(self):

        """Calculate win rate of trades"""

        total_trades = self.dataframe.count()
        # print("total_trades: ", total_trades)

        win_trades = (self.dataframe > 0).sum()
        # print("win trades: ", win_trades)

        win_rate = (win_trades / total_trades) * 100
        return win_rate

    def profit_factor(self):

        """Calculate profit factor of trades"""

        gross_profit = (self.dataframe[self.dataframe > 0]).sum()
        # print("gross profit: ", gross_profit)

        gross_loss = (self.dataframe[self.dataframe < 0]).sum()
        # print("gross profit: ", abs(gross_loss))

        pf = gross_profit / abs(gross_loss)
        return pf

    def avg_win_loss(self):

        """Calculate average win and loss"""

        win_trades = (self.dataframe > 0).sum()
        # print(f"win trades: {win_trades}")

        gross_profit = (self.dataframe[self.dataframe > 0]).sum()
        # print(f"gross profit: {gross_profit}")

        avg_win = gross_profit / win_trades
        # print(f"avg winn: {avg_win}")

        total_trades = self.dataframe.count()
        loss_trades = total_trades - win_trades
        # print(f"total_trades: {total_trades}, loss trades: {loss_trades}")

        gross_loss = (self.dataframe[self.dataframe < 0]).sum()
        # print("gross loss: ", abs(gross_loss))

        avg_loss = abs(gross_loss) / loss_trades
        # print(f"avg loss: {avg_loss}")

        return (avg_win, avg_loss)

    def max_dd():
        pass

    def max_loss_in_posit():
        pass

    def sharp():
        pass

    def correlation():
        pass
