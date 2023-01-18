import yfinance as yf


class GetStockData:
    def __init__(self, ticker, start, end):
        self.ticker = ticker
        self.start = start
        self.end = end

    def get_data(self):
        raw = yf.download(self.ticker, self.start, self.end)
        return raw


# stock = FinInstrument("T", "2020-11-01", "2022-01-01")

# get attribute, ticker
# print(stock.ticker)

# t_df = stock.get_data()
# print(t_df)
