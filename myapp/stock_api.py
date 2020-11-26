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


def get_stock_info(symbol, filter=()):
    # 'symbol,companyName,marketcap,totalCash,primaryExchange,latestPrice,latestSource,change,changePercent'
    try:
        return _request_data(f"/stable/stock/{symbol}/quote?{'' if not filter else ('filter=' + (','.join(filter)))}",
                             additional_parameters={'displayPercent': 'true'})
    except ConnectionError:
        raise StockServerUnReachable("Stock server UnReachable!")
    except Exception as e:
        for arg in e.args:
            if isinstance(arg, dict) and (b"Unknown symbol" in arg.values() or b"Not found" in arg.values()):
                raise StockSymbolNotFound("Stock symbol not found!")
        raise e


def get_stock_historic_prices(symbols, time_range='1m', chart_interval=None, filter=()):
    if time_range not in ALLOWED_TIME_RANGES:
        raise InvalidTimeRange("Invalid time range")
    try:
        if not chart_interval:
            if time_range == '6m':
                chart_interval = 3
            elif time_range.endswith('y'):
                chart_interval = int(time_range[0]) * 6
            elif time_range == 'max':
                chart_interval = 30
            else:
                chart_interval = 1
        response = _request_data(
            f'/stable/stock/market/batch?symbols={symbols}&types=chart&range={time_range}&'
            f'chartInterval={chart_interval}&includeToday=true&'
            f'{"" if not filter else ("filter=" + (",".join(filter)))}',
            additional_parameters={'displayPercent': 'true'})
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


def list_stocks_names(search_text, filter=()):
    try:
        if search_text:
            response = _request_data(f'/stable/search/{search_text}')
            symbols = ",".join([obj['symbol'] for obj in response])
            if symbols:
                response = _request_data(f'/stable/stock/market/batch?symbols={symbols}&types=quote&'
                                         f'{"" if not filter else ("filter=" + (",".join(filter)))}',
                                         additional_parameters={'displayPercent': 'true'})
                return [i['quote'] for i in response.values()]
        return []
    except ConnectionError:
        raise StockServerUnReachable("Stock server UnReachable!")


def get_analyst_recommendations(symbol):
    # 'ratingBuy, ratingOverweight, ratingHold, ratingUnderweight, ratingSell, ratingNone, ratingScaleMark'
    try:
        return _request_data(f'/stable/stock/{symbol}/recommendation-trends/')[0]
    except ConnectionError:
        raise StockServerUnReachable("Stock server UnReachable!")
    except Exception as e:
        for arg in e.args:
            if isinstance(arg, dict) and (b"Unknown symbol" in arg.values() or b"Not found" in arg.values()):
                raise StockSymbolNotFound("Stock symbol not found!")
        raise e