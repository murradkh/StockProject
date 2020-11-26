from myapp.models import Stock, WatchedStock, BoughtStock, SoldStock
from django.db.models import F
from myapp import stock_api
from django.db import transaction
from datetime import datetime

MAX_UNNEEDED_HISTORY_TO_PRESERVE_IN_PORTFOLIO = 20


def stock_api_update():
    start = datetime.now(datetime.now().astimezone().tzinfo)
    top_stock_update()
    update_existing_stocks()
    update_bought_stocks()
    delete_stocks(start)


@transaction.atomic
def top_stock_update():
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
    s = WatchedStock.objects.all().values("stock_id").distinct()
    for w in s:
        stock = Stock.objects.all().filter(symbol=w.get('stock_id'))[0]
        if (datetime.now(stock.last_modified.tzinfo) - stock.last_modified).total_seconds() > 5:
            data = stock_api.get_stock_info(stock.symbol)
            Stock.objects.filter(symbol=stock.symbol).update(
                name=data['companyName'],
                top_rank=None,
                price=data['latestPrice'],
                change=data['change'],
                change_percent=data['changePercent'],
                market_cap=data['marketCap'],
                primary_exchange=data['primaryExchange'],
                last_modified=datetime.now(stock.last_modified.tzinfo))


def update_bought_stocks():
    needed_bought_stocks = list(BoughtStock.objects.exclude(sold_quantity=F("quantity")))
    unneeded_bought_stocks_to_preserve = list(BoughtStock.objects.filter(sold_quantity=F("quantity")).order_by(
        "-created_on")[:MAX_UNNEEDED_HISTORY_TO_PRESERVE_IN_PORTFOLIO])
    for bought_stock in needed_bought_stocks + unneeded_bought_stocks_to_preserve:
        data = stock_api.get_stock_info(bought_stock.stock.symbol)
        Stock.objects.filter(symbol=bought_stock.stock.symbol).update(
            name=data['companyName'],
            top_rank=None,
            price=data['latestPrice'],
            change=data['change'],
            change_percent=data['changePercent'],
            market_cap=data['marketCap'],
            primary_exchange=data['primaryExchange'],
            last_modified=datetime.now(bought_stock.stock.last_modified.tzinfo))


def delete_stocks(time_threshold):
    stock = Stock.objects.all().filter(last_modified__lt=time_threshold)
    stock.delete()
