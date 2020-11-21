import time

from django.test import TestCase

from myapp.models import Stock, WatchedStock, User, ChangeStatusRule, Notification
from unittest import mock

from myapp.scheduler import scheduler
from myapp.scheduler.notification_msgs_updater import change_status_rule


class NotificationMsgsUpdaterTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        usr = User.objects.create_user(username='tester1',
                                       password='randomexample')
        stock = Stock.objects.create(symbol="SOLO",
                                     name='Electrameccanica Vehicles Corp',
                                     top_rank=1,
                                     price=10.0,
                                     change=2.0,
                                     change_percent=20.0)
        WatchedStock.objects.create(profile=usr.profile, stock=stock)

    @mock.patch("myapp.scheduler.notification_msgs_updater.stock_api")
    def test_change_status_rule(self, mocked_stock_api):
        """ checking positive change notification worked properly """
        watched_stock = WatchedStock.objects.get(pk=1)

        rule = ChangeStatusRule.objects.create(watched_stock=watched_stock, status='P', num_of_days=4,
                                               fired=False)
        dump_historical_data = [{'changePercent': 0, 'date': '2020-11-16'},
                                {'changePercent': 3.7105, 'date': '2020-11-17'},
                                {'changePercent': 7.4586, 'date': '2020-11-18'},
                                {'changePercent': 10.094, 'date': '2020-11-19'},
                                {'changePercent': 12.6157, 'date': '2020-11-20'}]
        mocked_stock_api.get_stock_historic_prices.return_value = dump_historical_data
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
        dump_historical_data = [{'changePercent': 0, 'date': '2020-11-16'},
                                {'changePercent': 3.7105, 'date': '2020-11-17'},
                                {'changePercent': 7.4586, 'date': '2020-11-18'},
                                {'changePercent': -10.094, 'date': '2020-11-19'},
                                {'changePercent': 12.6157, 'date': '2020-11-20'}]
        mocked_stock_api.get_stock_historic_prices.return_value = dump_historical_data
        change_status_rule()
        self.assertEqual(len(Notification.objects.filter(pk=2)), 0)

        rule = ChangeStatusRule.objects.create(watched_stock=watched_stock, status='N', num_of_days=5,
                                               fired=False)
        dump_historical_data = [{'changePercent': 0, 'date': '2020-11-16'},
                                {'changePercent': -3.7105, 'date': '2020-11-17'},
                                {'changePercent': -7.4586, 'date': '2020-11-18'},
                                {'changePercent': -10.094, 'date': '2020-11-19'},
                                {'changePercent': -12.6157, 'date': '2020-11-20'}]
        mocked_stock_api.get_stock_historic_prices.return_value = dump_historical_data
        change_status_rule()
        mocked_stock_api.get_stock_historic_prices.assert_called_with(symbols='SOLO', time_range='1m', chart_interval=1,
                                                                      filter=('changePercent', 'date'))
        self.assertEqual(len(Notification.objects.filter(pk=2)), 0)

        dump_historical_data.append({'changePercent': -12.6157, 'date': '2020-11-20'})
        change_status_rule()
        n = Notification.objects.get(pk=2)
        self.assertIsInstance(n, Notification)
        self.assertTrue("Negative" in n.title)
        self.assertTrue(str(rule.num_of_days) in n.description)
