from django.test import TestCase

from myapp.exceptions.stock_service import StockServerUnReachable, StockSymbolNotFound
from myapp.stock_api import get_stock_info


class StockApiTestCase(TestCase):

    def setUp(self):
        self.existed_symbols = ['AAL', 'WFC', "CCL"]
        self.not_existed_symbols = ['kamal', 'murad', 'malak']

    def test_service_is_up(self):
        try:
            get_stock_info('AAL')
        except StockServerUnReachable as e:
            raise AssertionError(e)

    def test_get_stock_info(self):
        for symbol in self.not_existed_symbols:
            self.assertRaises(StockSymbolNotFound, get_stock_info, symbol)
        for symbol in self.existed_symbols:
            response = get_stock_info(symbol)
            self.assertIsInstance(response, dict)

    def test_get_stock_historic_prices(self):
        for symbol in self.not_existed_symbols:
            self.assertRaises(StockSymbolNotFound, get_stock_info, symbol)
        for symbol in self.existed_symbols:
            response = get_stock_info(symbol)
            self.assertIsInstance(response, dict)

