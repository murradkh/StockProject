from django.test import TestCase

from myapp.exceptions.stock_service import StockServerUnReachable, StockSymbolNotFound
from myapp.stock_api import get_stock_info


class ViewsTestCase(TestCase):

    def setUp(self):
        self.existed_symbols = ['AAL', 'WFC', "CCL"]
        self.not_existed_symbols = ['kamal', 'murad', 'malak']

    def test_single_stock(self):
        for symbol in self.existed_symbols:
            response = self.client.get(f"/stock/{symbol}/")
            self.assertTemplateUsed(response, "single_stock.html")
            self.assertEquals(response.status_code, 200)
        for symbol in self.not_existed_symbols:
            response = self.client.get(f"/stock/{symbol}/")
            self.assertTemplateUsed(response, "exception.html")
            self.assertEquals(response.status_code, 404)

    def test_single_stock_historic(self):
        for symbol in self.existed_symbols:
            response = self.client.get(f"/historic/{symbol}/")
            self.assertContains(response, "data")
        for symbol in self.not_existed_symbols:
            response = self.client.get(f"/historic/{symbol}/")
            self.assertContains(response, "error_message", status_code=404)
