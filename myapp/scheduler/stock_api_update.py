from myapp.models import Stock
from myapp import stock_api
from django.db import transaction

from myapp.utilities import get_top_stocks_in_models_objects


@transaction.atomic
def stock_api_update():
    stocks_models = get_top_stocks_in_models_objects()
    for stock in stocks_models:
        stock.save()