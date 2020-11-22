import time

from django.test import TestCase

from myapp.models import Stock, WatchedStock, User, ChangeStatusRule, Notification, ChangeThresholdRule, \
    PriceThresholdRule
from unittest import mock

from myapp.scheduler import scheduler
from myapp.scheduler.notification_rules_handler import change_status_rule, change_threshold_rule, price_threshold_rule


class NotificationMsgsUpdaterTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        usr = User.objects.create_user(username='tester1',
                                       password='randomexample')
        stock_1 = Stock.objects.create(symbol="SOLO",
                                       name='Electrameccanica Vehicles Corp',
                                       top_rank=1,
                                       price=10.0,
                                       change=2.0,
                                       change_percent=20.0)
        stock_2 = Stock.objects.create(symbol="AAL",
                                       name='Electrameccanica Vehicles Corp',
                                       top_rank=1,
                                       price=10.0,
                                       change=2.0,
                                       change_percent=20.0)
        stock_3 = Stock.objects.create(symbol="SNAP",
                                       name='Electrameccanica Vehicles Corp',
                                       top_rank=1,
                                       price=10.0,
                                       change=2.0,
                                       change_percent=20.0)
        WatchedStock.objects.create(profile=usr.profile, stock=stock_1)
        WatchedStock.objects.create(profile=usr.profile, stock=stock_2)
        WatchedStock.objects.create(profile=usr.profile, stock=stock_3)

    @mock.patch("myapp.scheduler.notification_rules_handler.stock_api")
    def test_change_status_rule(self, mocked_stock_api):
        watched_stock = WatchedStock.objects.get(pk=1)

        rule = ChangeStatusRule.objects.create(watched_stock=watched_stock, status='P', num_of_days=4,
                                               fired=False)
        dump_data = [{'changePercent': 0, 'date': '2020-11-16'},
                     {'changePercent': 3.7105, 'date': '2020-11-17'},
                     {'changePercent': 7.4586, 'date': '2020-11-18'},
                     {'changePercent': 10.094, 'date': '2020-11-19'},
                     {'changePercent': 12.6157, 'date': '2020-11-20'}]
        mocked_stock_api.get_stock_historic_prices.return_value = dump_data
        change_status_rule()
        mocked_stock_api.get_stock_historic_prices.assert_called_with(symbols='SOLO', time_range='5d', chart_interval=1,
                                                                      filter=('changePercent', 'date'))
        n = Notification.objects.get(pk=1)
        self.assertIsInstance(n, Notification)
        self.assertTrue("Positive" in n.title)
        self.assertTrue(str(rule.num_of_days) in n.description)
        change_status_rule()
        mocked_stock_api.get_stock_historic_prices.assert_called_once()

        ChangeStatusRule.objects.create(watched_stock=watched_stock, status='P', num_of_days=4,
                                        fired=False)
        dump_data = [{'changePercent': 0, 'date': '2020-11-16'},
                     {'changePercent': 3.7105, 'date': '2020-11-17'},
                     {'changePercent': 7.4586, 'date': '2020-11-18'},
                     {'changePercent': -10.094, 'date': '2020-11-19'},
                     {'changePercent': 12.6157, 'date': '2020-11-20'}]
        mocked_stock_api.get_stock_historic_prices.return_value = dump_data
        change_status_rule()
        self.assertEqual(len(Notification.objects.filter(pk=2)), 0)

        rule = ChangeStatusRule.objects.create(watched_stock=watched_stock, status='N', num_of_days=5,
                                               fired=False)
        dump_data = [{'changePercent': 0, 'date': '2020-11-16'},
                     {'changePercent': -3.7105, 'date': '2020-11-17'},
                     {'changePercent': -7.4586, 'date': '2020-11-18'},
                     {'changePercent': -10.094, 'date': '2020-11-19'},
                     {'changePercent': -12.6157, 'date': '2020-11-20'}]
        mocked_stock_api.get_stock_historic_prices.return_value = dump_data
        change_status_rule()
        mocked_stock_api.get_stock_historic_prices.assert_called_with(symbols='SOLO', time_range='1m', chart_interval=1,
                                                                      filter=('changePercent', 'date'))
        self.assertEqual(len(Notification.objects.filter(pk=2)), 0)

        dump_data.append({'changePercent': -12.6157, 'date': '2020-11-20'})
        change_status_rule()
        n = Notification.objects.get(pk=2)
        self.assertIsInstance(n, Notification)
        self.assertTrue("Negative" in n.title)
        self.assertTrue(str(rule.num_of_days) in n.description)

    @mock.patch("myapp.scheduler.notification_rules_handler.stock_api")
    def test_threshold_rule(self, mocked_stock_api):
        watched_stock = WatchedStock.objects.get(pk=1)

        # Below threshold testing
        rule = ChangeThresholdRule.objects.create(watched_stock=watched_stock, when='B', percentage_threshold=20,
                                                  fired=False)
        dump_data = {'changePercent': 12.638}
        mocked_stock_api.get_stock_info.return_value = dump_data
        change_threshold_rule()
        mocked_stock_api.get_stock_info.assert_called_with(symbol=rule.watched_stock.stock.symbol,
                                                           filter=("changePercent",))
        n = Notification.objects.get(pk=1)
        self.assertIsInstance(n, Notification)
        self.assertTrue("Below" in n.title)
        self.assertTrue(str(rule.percentage_threshold) in n.description)
        self.assertTrue(str(round(dump_data['changePercent'])) in n.description)

        # checking the notification would be called once
        change_status_rule()
        mocked_stock_api.get_stock_info.assert_called_once()

        ChangeThresholdRule.objects.create(watched_stock=watched_stock, when='B', percentage_threshold=20,
                                           fired=False)
        dump_data = {'changePercent': 22.638}
        mocked_stock_api.get_stock_info.return_value = dump_data
        change_threshold_rule()
        self.assertEqual(len(Notification.objects.filter(pk=2)), 0)

        # Above threshold testing
        watched_stock = WatchedStock.objects.get(pk=2)
        rule = ChangeThresholdRule.objects.create(watched_stock=watched_stock, when='A', percentage_threshold=-20,
                                                  fired=False)
        dump_data = {'changePercent': -12}
        mocked_stock_api.get_stock_info.return_value = dump_data
        change_threshold_rule()
        mocked_stock_api.get_stock_info.assert_called_with(symbol=rule.watched_stock.stock.symbol,
                                                           filter=("changePercent",))
        n = Notification.objects.get(pk=3)
        self.assertIsInstance(n, Notification)
        self.assertTrue("Above" in n.title)
        self.assertTrue(str(rule.percentage_threshold) in n.description)
        self.assertTrue(str(round(dump_data['changePercent'])) in n.description)

        ChangeThresholdRule.objects.create(watched_stock=watched_stock, when='A', percentage_threshold=20,
                                           fired=False)
        dump_data = {'changePercent': 19.638}
        mocked_stock_api.get_stock_info.return_value = dump_data
        change_threshold_rule()
        self.assertEqual(len(Notification.objects.filter(pk=4)), 0)

        # On Threshold testing
        watched_stock = WatchedStock.objects.get(pk=3)
        rule = ChangeThresholdRule.objects.create(watched_stock=watched_stock, when='O', percentage_threshold=99.4,
                                                  fired=False)
        dump_data = {'changePercent': 99.4}
        mocked_stock_api.get_stock_info.return_value = dump_data
        change_threshold_rule()
        mocked_stock_api.get_stock_info.assert_called_with(symbol=rule.watched_stock.stock.symbol,
                                                           filter=("changePercent",))
        n = Notification.objects.get(pk=5)
        self.assertIsInstance(n, Notification)
        self.assertTrue("On" in n.title)
        self.assertTrue(str(rule.percentage_threshold) in n.description)
        self.assertTrue(str(dump_data['changePercent']) in n.description)

        ChangeThresholdRule.objects.create(watched_stock=watched_stock, when='O', percentage_threshold=10,
                                           fired=False)
        dump_data = {'changePercent': 11}
        mocked_stock_api.get_stock_info.return_value = dump_data
        change_threshold_rule()
        self.assertEqual(len(Notification.objects.filter(pk=6)), 0)

    @mock.patch("myapp.scheduler.notification_rules_handler.stock_api")
    def test_price_threshold_rule(self, mocked_stock_api):
        watched_stock = WatchedStock.objects.get(pk=1)

        # Below threshold testing
        rule = PriceThresholdRule.objects.create(watched_stock=watched_stock, when='B', price_threshold=20,
                                                 fired=False)
        dump_data = {'latestPrice': 12.638}
        mocked_stock_api.get_stock_info.return_value = dump_data
        price_threshold_rule()
        mocked_stock_api.get_stock_info.assert_called_with(symbol=rule.watched_stock.stock.symbol,
                                                           filter=("latestPrice",))
        n = Notification.objects.get(pk=1)
        self.assertIsInstance(n, Notification)
        self.assertTrue("Below" in n.title)
        self.assertTrue(str(rule.price_threshold) in n.description)
        self.assertTrue(str(dump_data['latestPrice']) in n.description)

        # checking the notification would be called once
        price_threshold_rule()
        mocked_stock_api.get_stock_info.assert_called_once()

        rule = PriceThresholdRule.objects.create(watched_stock=watched_stock, when='B', price_threshold=12,
                                                 fired=False)
        dump_data = {'latestPrice': 12.638}
        mocked_stock_api.get_stock_info.return_value = dump_data
        price_threshold_rule()
        self.assertEqual(len(Notification.objects.filter(pk=2)), 0)

        # Above threshold testing
        watched_stock = WatchedStock.objects.get(pk=2)
        rule = PriceThresholdRule.objects.create(watched_stock=watched_stock, when='A', price_threshold=12,
                                                 fired=False)
        dump_data = {'latestPrice': 12.638}
        mocked_stock_api.get_stock_info.return_value = dump_data
        price_threshold_rule()
        mocked_stock_api.get_stock_info.assert_called_with(symbol=rule.watched_stock.stock.symbol,
                                                           filter=("latestPrice",))
        n = Notification.objects.get(pk=2)
        self.assertIsInstance(n, Notification)
        self.assertTrue("Above" in n.title)
        self.assertTrue(str(rule.price_threshold) in n.description)
        self.assertTrue(str(dump_data['latestPrice']) in n.description)

        rule = PriceThresholdRule.objects.create(watched_stock=watched_stock, when='A', price_threshold=20,
                                                 fired=False)
        dump_data = {'latestPrice': 14}
        mocked_stock_api.get_stock_info.return_value = dump_data
        price_threshold_rule()
        self.assertEqual(len(Notification.objects.filter(pk=3)), 0)

        # On Threshold testing
        watched_stock = WatchedStock.objects.get(pk=3)
        rule = PriceThresholdRule.objects.create(watched_stock=watched_stock, when='O', price_threshold=18,
                                                 fired=False)
        dump_data = {'latestPrice': 18}
        mocked_stock_api.get_stock_info.return_value = dump_data
        price_threshold_rule()
        mocked_stock_api.get_stock_info.assert_called_with(symbol=rule.watched_stock.stock.symbol,
                                                           filter=("latestPrice",))
        n = Notification.objects.get(pk=3)
        self.assertIsInstance(n, Notification)
        self.assertTrue("On" in n.title)
        self.assertTrue(str(rule.price_threshold) in n.description)
        self.assertTrue(str(dump_data['latestPrice']) in n.description)

        rule = PriceThresholdRule.objects.create(watched_stock=watched_stock, when='O', price_threshold=18,
                                                 fired=False)
        dump_data = {'latestPrice': 18.2}
        mocked_stock_api.get_stock_info.return_value = dump_data
        price_threshold_rule()
        self.assertEqual(len(Notification.objects.filter(pk=4)), 0)
