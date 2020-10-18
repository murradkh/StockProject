from myapp.models import Stock
from myapp import stock_api
from django.db import transaction


@transaction.atomic
def stock_api_update():
    top_stocks = stock_api._get_top_stocks()
    index = 1
    try:
        for stock in top_stocks:
            # This searches for a stock with the given 'symbol' (the primary key)
            # and updates/create it with the values specified in the 'defaults' parameter
            stock_model, created = Stock.objects.update_or_create(symbol=stock['symbol'], defaults={
                'name': stock['companyName'],
                'top_rank': index,
                'price': stock['latestPrice'],
                'change': stock['change'],
                'change_percent': stock['changePercent'],
                'market_cap': stock['marketCap'],
                'primary_exchange': stock['primaryExchange'],
            })
            stock_model.save()
            index += 1
    except KeyError as error:
        pass
