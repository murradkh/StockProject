from django.test import TestCase
from datetime import datetime
from myapp.exceptions.stock_service import StockServerUnReachable, StockSymbolNotFound
from myapp.stock_api import get_stock_info, get_stock_historic_prices, get_top_stocks, list_stocks_names
from myapp.views import STOCKS_PER_PAGE


class StockApiTestCase(TestCase):

    def setUp(self):
        self.existed_symbols = ['AAL', 'WFC', "DFS"]
        self.not_existed_symbols = ['kamal', 'murad', 'malak']

    def test_service_is_up(self):
        try:
            get_stock_info(self.existed_symbols[0])
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
            self.assertRaises(StockSymbolNotFound, get_stock_historic_prices, symbol)
        for symbol in self.existed_symbols:
            response = get_stock_historic_prices(symbol)
            self.assertIsInstance(response, list)
        response = get_stock_historic_prices(",".join(self.existed_symbols + self.not_existed_symbols))
        self.assertEquals(len(response), len(self.existed_symbols))
        response = get_stock_historic_prices("," + self.existed_symbols[0] + ",")
        self.assertIsInstance(response, list)

        # testing time range
        response = get_stock_historic_prices(self.existed_symbols[0], '1y')
        first_year = datetime.fromisoformat(response[0].get('date')).year
        second_year = datetime.today().year
        self.assertEquals(second_year - first_year, 1)
        response = get_stock_historic_prices(self.existed_symbols[0], '1m')
        first_month = datetime.fromisoformat(response[0].get('date')).month
        second_month = datetime.today().month
        self.assertEquals(second_month - first_month, 1)

    def test_get_top_stocks(self):
        response = get_top_stocks()
        self.assertIsInstance(response, list)

    def test_list_stocks_names(self):
        response = list_stocks_names("A")
        self.assertIsInstance(response, list)
        self.assertEquals(len(response), 10)
        response = list_stocks_names("snap-mm")
        self.assertIsInstance(response, list)
        self.assertEquals(len(response), 1)
        response = list_stocks_names("unknown")
        self.assertIsInstance(response, list)
        self.assertEquals(len(response), 0)
        response = list_stocks_names(" ")
        self.assertIsInstance(response, list)
        self.assertEquals(len(response), 0)
        self.assertRaises(Exception, list_stocks_names, "")
