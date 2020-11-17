from myapp.models import Stock, Profile
from myapp import stock_api
from django.db import transaction
from django.db import connection

@transaction.atomic
def stock_api_update():
    update_existing_stocks()
    top_stocks = stock_api.get_top_stocks()
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
    except KeyError as e:
        pass


def update_existing_stocks():
    # each profile
    p = Profile.objects.all()#[0].watchlist.all()
    # for stock in p:
    #     print(stock.symbol)
    stocks = set()
    for w in p:
        for stock in w.watchlist.all():
                stocks.add(stock.symbol)
    print(stocks)

    # objs = [
    #     Entry.objects.create(headline='Entry 1'),
    #     Entry.objects.create(headline='Entry 2'),
    # ]
    # objs[0].headline = 'This is entry 1'
    # objs[1].headline = 'This is entry 2'
    # Entry.objects.bulk_update(objs, ['headline'])

    # for p in Profile.watchlist.raw('SELECT distinct * FROM myapp_profile_watchlist'):
    #     print(p)
    # cursor = connection.cursor()
    # cursor.execute('''SELECT distinct * FROM myapp_profile_watchlist''')
    # row = cursor.feachall()
    # print(row)

# def get_stock_info(symbol):
# 'symbol,companyName,marketcap,totalCash,primaryExchange,latestPrice,latestSource,change,changePercent'
