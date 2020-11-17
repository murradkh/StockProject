from django.contrib.auth.models import User
from django.test import Client, TestCase
from myapp.models import Profile, Stock, WatchedStock


class NotificationModelsRulesTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass
        # self.test_user_1 = User.objects.create_user(username='tester1',
        #                                             password='randomexample')
        # WatchedStock.objects.create()
    def test_change_status_rule(self):

        # assertQuerysetEqual
        pass