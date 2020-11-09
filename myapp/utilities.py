from myapp import stock_api
from myapp.models import Stock


def get_top_stocks_in_models_objects():
    top_stocks = stock_api.get_top_stocks()
    index = 1
    stocks_models = []
    try:
        for stock in top_stocks:
            stock_model, created = Stock.objects.update_or_create(symbol=stock['symbol'], defaults={
                'name': stock['companyName'],
                'top_rank': index,
                'price': stock['latestPrice'],
                'change': stock['change'],
                'change_percent': stock['changePercent'],
                'market_cap': stock['marketCap'],
                'primary_exchange': stock['primaryExchange'],
            })
            index += 1
            stocks_models.append(stock_model)
        return stocks_models
    except KeyError as e:
        pass