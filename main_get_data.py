import pandas as pd

from get_data.get_stock_data import GetStockData
from get_data.get_crypto_futures_data import GetCryptoFutData


# Stock
"""
tickers = ["MSFT", "BA"]
start_date = "2022-01-01"
end_date = "2023-07-01"
path = "datafeed"

# create class instance, for get 1 or more stokcs
stock = GetStockData(tickers, start_date, end_date, path)

# get data
df = stock.get_data()
print(stock.ticker)
"""

tickers_crypto = [
    "BTCUSDT",
    "ETHUSDT",
    "XRPUSDT",
    "1000SHIBUSDT",
    "CRVUSDT",
    "SOLUSDT",
    "DOGEUSDT",
    "LTCUSDT",
    "OPUSDT",
    "STMXUSDT",
    "COMPUSDT",
    "MKRUSDT",
    "BCHUSDT",
    "TOMOUSDT",
    "LINKUSDT",
    "1000PEPEUSDT",
    "BNBUSDT",
    "ARBUSDT",
    "MATICUSDT",
    "KNCUSDT",
    "XLMUSDT",
    "FXSUSDT",
    "DYDXUSDT",
    "LINAUSDT",
    "ADAUSDT",
    "SNXUSDT",
    "AAVEUSDT",
    "EOSUSDT",
    "SUIUSDT",
    "CFXUSDT",
    "FILUSDT",
    "INJUSDT",
    "APTUSDT",
    "GALAUSDT",
    "APEUSDT",
    "ETCUSDT",
    "UNIUSDT",
    "AVAXUSDT",
    "WAVESUSDT",
    "OGNUSDT",
    "WOOUSDT",
    "MASKUSDT",
    "DOTUSDT",
    "CELOUSDT",
    "SANDUSDT",
    "MTLUSDT",
    "ATOMUSDT",
    "FTMUSDT",
    "LDOUSDT",
    "NEARUSDT",
    "BAKEUSDT",
    "AXSUSDT",
    "TRXUSDT",
    "GMTUSDT",
    "XVGUSDT",
    "XMRUSDT",
    "ANTUSDT",
    "STGUSDT",
    "XEMUSDT",
    "ALGOUSDT",
    "RNDRUSDT",
    "YFIUSDT",
    "STXUSDT",
    "1INCHUSDT",
    "GMXUSDT",
    "FLOWUSDT",
    "HBARUSDT",
    "MANAUSDT",
    "KAVAUSDT",
    "GRTUSDT",
    "SUSHIUSDT",
    "EDUUSDT",
    "AGIXUSDT",
    "1000LUNCUSDT",
    "QTUMUSDT",
    "BATUSDT",
    "C98USDT",
    "HIGHUSDT",
    "ASTRUSDT",
    "STORJUSDT",
    "LQTYUSDT",
    "UNFIUSDT",
    "XTZUSDT",
    "OMGUSDT",
    "IMXUSDT",
    "ZENUSDT",
    "ENSUSDT",
    "COTIUSDT",
    "IDUSDT",
    "FETUSDT",
    "FLMUSDT",
    "ARPAUSDT",
    "CHZUSDT",
    "DENTUSDT",
    "API3USDT",
    "CVXUSDT",
    "KSMUSDT",
    "ARKMUSDT",
    "OCEANUSDT",
    "MAVUSDT",
    "THETAUSDT",
    "LUNA2USDT",
    "ICPUSDT",
    "GTCUSDT",
    "JASMYUSDT",
    "ANKRUSDT",
    "USDCUSDT",
    "SFPUSDT",
    "AGLDUSDT",
    "NEOUSDT",
    "RDNTUSDT",
    "ZILUSDT",
    "ENJUSDT",
    "JOEUSDT",
    "SXPUSDT",
    "CTSIUSDT",
    "GALUSDT",
    "DASHUSDT",
    "TUSDT",
    "ACHUSDT",
    "RSRUSDT",
    "1000XECUSDT",
    "ZRXUSDT",
    "RUNEUSDT",
    "VETUSDT",
    "PEOPLEUSDT",
    "LITUSDT",
    "BELUSDT",
    "ATAUSDT",
    "HOOKUSDT",
    "IOTXUSDT",
    "ALPHAUSDT",
    "TRBUSDT",
    "ROSEUSDT",
    "EGLDUSDT",
    "BLURUSDT",
    "LRCUSDT",
    "ZECUSDT",
    "ALICEUSDT",
    "CHRUSDT",
    "SSVUSDT",
    "ONTUSDT",
    "MINAUSDT",
    "ONEUSDT",
    "COMBOUSDT",
    "PHBUSDT",
    "ICXUSDT",
    "DARUSDT",
    "BANDUSDT",
    "REEFUSDT",
    "IOTAUSDT",
    "BNXUSDT",
    "CELRUSDT",
    "QNTUSDT",
    "SKLUSDT",
    "RENUSDT",
    "HOTUSDT",
    "AUDIOUSDT",
    "HFTUSDT",
    "FOOTBALLUSDT",
    "AMBUSDT",
    "TLMUSDT",
    "DUSKUSDT",
    "KLAYUSDT",
    "1000FLOKIUSDT",
    "NKNUSDT",
    "ARUSDT",
    "BALUSDT",
    "PENDLEUSDT",
    "SPELLUSDT",
    "RADUSDT",
    "TRUUSDT",
    "KEYUSDT",
    "DGBUSDT",
    "PERPUSDT",
    "LPTUSDT",
    "LEVERUSDT",
    "RLCUSDT",
    "UMAUSDT",
]

print(len(tickers_crypto))


# Crypto (futures)
# ticker_crypto = "ETHUSDT"
time_frame = "1d"
limit_rows = 1500
start_date_crypto = "2019-01-01 00:00:00"
path = "datafeed/crypto"


for ticker in tickers_crypto:
    crypto_fut_data = GetCryptoFutData(
        ticker, time_frame, limit_rows, start_date_crypto
    )
    df_usdt = crypto_fut_data.get_futures_data()
    df_usdt.index.name = "Date"
    print(df_usdt)

    df_usdt.to_csv(f"{path}/{ticker}.csv")
