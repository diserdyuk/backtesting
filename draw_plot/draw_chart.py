import matplotlib.pyplot as plt


class DrawChart:

    """Class for drawing charts

    Attributes
    ----------
    ticker: str
        symbol of instrument

    Methods
    -------
    draw_chart:
        drawing one chart (time and price)
    """

    def __init__(self, ticker, data, df, save_path):
        self.ticker = ticker
        self.data = data
        self.df = df
        self.save_path = save_path

    def draw_chart(self):
        self.data.plot(kind="line", figsize=[14, 8])
        plt.title(
            f"{self.ticker}, period: {self.df.iloc[0][0]} - {self.df.iloc[-1][0]}",
            fontsize=13,
        )
        plt.tight_layout()
        plt.savefig(f"{self.save_path}/{self.ticker}.png")
        # plt.show()
