from django.test import TestCase, Client
from myapp.models import Stock


class SingleStockTestCase(TestCase):
    def setUp(self):            # NOTE: Optional function for setting up initial conditions
        Stock.objects.create(
            symbol="GE",
            name='General Electric',
            top_rank=1,
            price=10.0,
            change=1.0,
            change_percent=15.0
        )

    def test_get_stock(self):   # NOTE: Test function name must always start with test_
        c = Client()
        response = c.get('/stock/GE/')
        self.assertEquals(response.status_code, 200)
