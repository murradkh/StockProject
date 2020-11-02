from .exceptions.stock_service import StockServerUnReachable, StockSymbolNotFound
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


def get_stock_historic_prices(symbols, time_range='1m'):
    try:
        response = _request_data('/stable/stock/market/batch?symbols={symbols}&types=chart&range={time_range}'.format(
            symbols=symbols, time_range=time_range))
        if len(response) == 1:
            return response.popitem()[1]['chart']
        return response
    except ConnectionError:
        raise StockServerUnReachable("Stock server UnReachable!")
    except Exception as e:
        for arg in e.args:
            if isinstance(arg, dict) and (b"Unknown symbol" in arg.values() or b"Not found" in arg.values()):
                raise StockSymbolNotFound("Unknown Stock Symbol!")
        raise e


def list_stocks_names(search_text):
    try:
        response = _request_data(f'/stable/search/{search_text}')
        symbols = ",".join([obj['symbol'] for obj in response])
        if symbols:
            response = _request_data(f'/stable/stock/market/batch?symbols={symbols}&types=quote&filter=symbol,'
                                     f'companyName')
            return [i['quote'] for i in response.values()]
        return []
    except ConnectionError:
        raise StockServerUnReachable("Stock server UnReachable!")
    except Exception as e:
        for arg in e.args:
            if isinstance(arg, dict) and (b"Unknown symbol" in arg.values() or b"Not found" in arg.values()):
                raise StockSymbolNotFound("Stock symbol not found!")
        raise e
