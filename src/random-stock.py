"""
Semplicemente, restituice una stock random
"""

from libs.companies import stock_markets
from libs.utilities import get_random_stock

STOCK_MARKET_NAME = "nasdaq100"
STOCK_MARKET = stock_markets[STOCK_MARKET_NAME]

stock_name, stock_symbol = get_random_stock(stocks_list=STOCK_MARKET)

print(f"Random stock: {stock_name} ({stock_symbol})")