from django.test import TestCase
from datetime import datetime
from myapp.exceptions.stock_service import StockServerUnReachable, StockSymbolNotFound, InvalidTimeRange
from myapp.stock_api import get_stock_info, get_stock_historic_prices, get_top_stocks,list_stocks_names


MAX_DAYS_PER_MONTH = 31
MAX_DAYS_PER_YEAR = 366  # On a leap year


class StockApiTestCase(TestCase):

    def setUp(self):
        self.existed_symbols = ['AAL', 'WFC', "DFS"]
        self.not_existed_symbols = ['kamal', 'murad', 'malak']

        self.valid_time_ranges = ['1d', '5d', '1m', '3m', '6m', '1y', '5y']
        self.invalid_time_ranges = ['1x', '42z', 'rt', 'test']


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


    def test_get_stock_historic_prices_symbol(self):
        for symbol in self.not_existed_symbols:
            self.assertRaises(StockSymbolNotFound, get_stock_historic_prices, symbol)
        for symbol in self.existed_symbols:
            response = get_stock_historic_prices(symbol)
            self.assertIsInstance(response, list)
        response = get_stock_historic_prices(",".join(self.existed_symbols + self.not_existed_symbols))
        self.assertEquals(len(response), len(self.existed_symbols))
        response = get_stock_historic_prices("," + self.existed_symbols[0] + ",")
        self.assertIsInstance(response, list)


    def test_get_stock_historic_prices_time(self):
        for time_range in self.valid_time_ranges:
            response = get_stock_historic_prices(self.existed_symbols[0], time_range)

            first_date = datetime.fromisoformat(response[0].get('date'))
            final_date = datetime.fromisoformat(response[-1].get('date'))
            days_returned = len(response)

            today = datetime.now()
            days_since_last_result = (today - final_date).days

            if time_range.endswith('d'):
                if time_range == '1d':
                    self.assertEquals((final_date - first_date).days, 0)
                elif time_range == '5d':
                    self.assertLessEqual(days_returned, 7)

                if today.weekday() in list(range(1, 6)):    # if between Tuesday and Saturday
                    self.assertLessEqual(days_since_last_result, 1)

            elif time_range.endswith('m'):
                self.assertLessEqual(days_returned, int(time_range[0]) * MAX_DAYS_PER_MONTH)

            elif time_range.endswith('y'):
                self.assertLessEqual(days_returned, int(time_range[0]) * MAX_DAYS_PER_YEAR)


        for time_range in self.invalid_time_ranges:
            self.assertRaises(InvalidTimeRange, get_stock_historic_prices, self.existed_symbols[0], time_range)


    def test_get_top_stocks(self):
        response = get_top_stocks()
        self.assertIsInstance(response, list)

    def test_list_stocks_names(self):
        response = list_stocks_names("A")
        self.assertIsInstance(response, list)
        self.assertGreater(len(response), 1)
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
