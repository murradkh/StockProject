from .exceptions.stock_service import StockServerUnReachable, StockSymbolNotFound, InvalidTimeRange
from requests.exceptions import ConnectionError
import requests

# Sandbox API - FOR TESTING
BASE_URL = 'https://sandbox.iexapis.com'
PUBLIC_TOKEN = 'Tpk_c818732500c24764801eb121fa658bb6'

# Real API - FOR PRODUCTION
# YOU NEED TO CREATE AN ACCOUNT TO RECEIVE YOUR OWN API KEYS (its free)
# BASE_URL = '<MAKE_AN_ACCOUNT>'
# PUBLIC_TOKEN = '<MAKE_AN_ACCOUNT>'

# For general info for all symbols
# https://cloud.iexapis.com/stable/ref-data/symbols?token=pk_dd07f5a1aaea4a039cfe8118f3d9727a


# For all symbols with prices (*free weight*)
# https://cloud.iexapis.com/stable/tops/last?token=pk_dd07f5a1aaea4a039cfe8118f3d9727a

STOCKS_AMOUNT_TO_FETCH = 200
ALLOWED_TIME_RANGES = ['max', '5y', '2y', '1y', 'ytd', '6m', '3m', '1m', '1mm', '5d', '5dm', '1d']


def _request_data(url, filter='', additional_parameters={}):
    final_url = BASE_URL + url

    query_strings = {
        'token': PUBLIC_TOKEN
    }
    query_strings.update(additional_parameters)

    if filter:
        query_strings['filter'] = filter

    response = requests.get(final_url, params=query_strings)

    if not response.ok:
        raise Exception('Unexpected response: ', response.__dict__)
    return response.json()


def get_top_stocks():
    try:
        return _request_data('/stable/stock/market/list/mostactive',
                             filter='symbol,companyName,latestVolume,change,changePercent,primaryExchange,marketCap,'
                                    'latestPrice,calculationPrice',
                             additional_parameters={'displayPercent': 'true', 'listLimit': STOCKS_AMOUNT_TO_FETCH})
    except ConnectionError:
        raise StockServerUnReachable("Stock server UnReachable!")
    except Exception as e:
        for arg in e.args:
            if isinstance(arg, dict) and (b"Unknown symbol" in arg.values() or b"Not found" in arg.values()):
                raise StockSymbolNotFound("Stock symbol not found!")
        raise e


def get_stock_info(symbol):
    # 'symbol,companyName,marketcap,totalCash,primaryExchange,latestPrice,latestSource,change,changePercent'
    try:
        return _request_data('/stable/stock/{symbol}/quote'.format(symbol=symbol),
                             additional_parameters={'displayPercent': 'true'})
    except ConnectionError:
        raise StockServerUnReachable("Stock server UnReachable!")
    except Exception as e:
        for arg in e.args:
            if isinstance(arg, dict) and (b"Unknown symbol" in arg.values() or b"Not found" in arg.values()):
                raise StockSymbolNotFound("Stock symbol not found!")
        raise e


def get_stock_historic_prices(symbol, time_range='1m'):
    if time_range not in ALLOWED_TIME_RANGES:
        raise InvalidTimeRange("Invalid time range")
    try:
        return _request_data('/stable/stock/{symbol}/chart/{time_range}'.format(symbol=symbol, time_range=time_range))
    except ConnectionError:
        raise StockServerUnReachable("Stock server UnReachable!")
    except Exception as e:
        for arg in e.args:
            if isinstance(arg, dict) and (b"Unknown symbol" in arg.values() or b"Not found" in arg.values()):
                raise StockSymbolNotFound("Unknown Stock Symbol!")
        raise e
