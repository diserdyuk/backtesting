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
