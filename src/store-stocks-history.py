from libs.companies import stock_markets
from libs.database import create_db_if_not_exists
import yfinance as yf
from libs.database import store_stock_history

STOCK_MARKET_NAME = "nasdaq100"
STOCK_MARKET = stock_markets[STOCK_MARKET_NAME]

create_db_if_not_exists()

for stock, ticker in STOCK_MARKET.items():
    print(f"Store stock history for ticker {ticker}")
    
    history = yf.Ticker(ticker).history(period='max')

    store_stock_history(ticker, stock_history=history)