from libs.companies import stock_markets
from libs.utilities import store_stock_history

STOCK_MARKET_NAME = "nasdaq100"
STOCK_MARKET = stock_markets[STOCK_MARKET_NAME]

for stock, ticker in STOCK_MARKET.items():
    print(f"Store stock history for ticker {ticker}")
    store_stock_history(ticker)