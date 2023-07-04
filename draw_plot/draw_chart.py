import matplotlib.pyplot as plt


class DrawChart:

    """Class for drawing charts

    Attributes
    ----------
    ticker: str
        symbol of instrument
    data: dataframe
        DataFrame
    title: define plot
        title of plot
    xlabel and ylabel:
        name of axis plot
    save_path:
        dir for chart

    Methods
    -------
    plot_data:
        drawing one chart (time and price)
    """

    def __init__(self, ticker, data, title, xlabel, ylabel, save_path):
        self.ticker = ticker
        self.data = data
        self.title = title
        self.save_path = save_path
        self.xlabel = xlabel
        self.ylabel = ylabel

    def plot_data(self):
        """plot stock prices"""
        plt.rcParams["figure.figsize"] = (12, 8)

        ax = self.data.plot(title=f"{self.title}_{self.ticker}", fontsize=9)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        plt.tight_layout()
        plt.savefig(f"{self.save_path}/{self.title}_{self.ticker}.png")
