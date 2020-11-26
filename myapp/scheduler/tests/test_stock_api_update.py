from unittest import TestCase

from ..stock_api_update import stock_api_update
from ...models import Stock


class JbsTestCase(TestCase):

    def test_api_update(self):
        stock_api_update()
        value_1 = Stock.objects.filter(top_rank=1)[0].last_modified
        stock_api_update()
        value_2 = Stock.objects.filter(top_rank=1)[0].last_modified
        self.assertNotEqual(value_1, value_2)
