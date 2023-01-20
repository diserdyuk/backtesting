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

    def __init__(self, ticker, data):
        self.ticker = ticker
        self.data = data

    def draw_chart(self):
        self.data.plot(figsize=(14, 8))
        plt.title(f"{self.ticker}", fontsize=13)
        plt.tight_layout()
        plt.savefig(f"{self.ticker}.png")
        # plt.show()
