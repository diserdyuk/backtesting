import numpy as np


def log_return(data):

    """
    Function calculate log return (np.log) on base Close price

    Params
    ----------
    data: DataFrame
        using column 'Close' price
    """

    data["Log_return"] = np.log(data.Close / data.Close.shift(1))
    return data


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
