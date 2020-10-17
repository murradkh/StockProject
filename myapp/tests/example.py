from django.test import TestCase, Client
from myapp.models import Stock


class SingleStockTestCase(TestCase):  # If your class doesn't use a database, use SimpleTestCase to inherit from
    fixtures = ['stocks.json']

    @classmethod
    def setUpTestData(cls):  # allows the creation of initial data at the class level, once for the whole TestCase.
        Stock.objects.create(
            symbol="GE",
            name='General Electric',
            top_rank=1,
            price=10.0,
            change=1.0,
            change_percent=15.0
        )

    def setUp(self):  # NOTE: Optional function for setting up initial setups
        pass

    def test_get_stock(self):  # NOTE: Test function name must always start with test_
        # this instance creation is unneeded when the class inheriting from TestCase, it has a default one "self.client"
        response = self.client.get('/stock/GE/')
        self.assertEqual(response.status_code, 200)
