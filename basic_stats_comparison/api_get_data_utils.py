import yfinance as yf
from yfinance.utils import get_json


def create_ticker_name_to_info(ticker_names):
    ticker_name_to_info = {}
    for name in ticker_names:
        ticker = yf.Ticker(name)
        ticker_info = ticker.info
        ticker_name_to_info[name] = ticker_info
    return ticker_name_to_info


def create_ticker_name_to_data(ticker_names):
    # debug for missing info
    # this allow to get some missing info e.g. expense ratio for etf
    _SCRAPE_URL_ = 'https://finance.yahoo.com/quote'
    ticker_name_to_data = {}
    for name in ticker_names:
        ticker_url = "{}/{}".format(_SCRAPE_URL_, name)
        ticker_data = get_json(url=ticker_url)
        ticker_name_to_data[name] = ticker_data
    return ticker_name_to_data
