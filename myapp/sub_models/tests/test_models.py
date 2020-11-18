from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from myapp.models import Profile, Stock, WatchedStock, ChangeStatusRule, ChangeThresholdRule, PriceThresholdRule, \
    RecommendationAnalystRule


class NotificationModelsRulesTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        usr = User.objects.create_user(username='tester1',
                                       password='randomexample')
        stock = Stock.objects.create(symbol="APPL",
                                     name='Apple',
                                     top_rank=1,
                                     price=10.0,
                                     change=2.0,
                                     change_percent=20.0)
        watched_stock = WatchedStock.objects.create(profile=usr.profile, stock=stock)

    def test_change_status_rule(self):
        # assertQuerysetEqual
        watched_stock = WatchedStock.objects.get(pk=1)
        ChangeStatusRule(watched_stock=watched_stock, status='N', num_of_days=4, fired=False).full_clean()
        ChangeStatusRule(watched_stock=watched_stock, status='P', num_of_days=4, fired=False).full_clean()
        self.assertRaises(ValidationError, ChangeStatusRule(watched_stock=watched_stock, status='D',
                                                            num_of_days=4,
                                                            fired=False).full_clean)
        self.assertRaises(ValidationError, ChangeStatusRule(status='P',
                                                            num_of_days=361,
                                                            fired=False).full_clean)
        self.assertRaises(ValidationError, ChangeStatusRule(status='P',
                                                            num_of_days=1,
                                                            fired=False).full_clean)

    def test_change_threshold_rule(self):
        watched_stock = WatchedStock.objects.get(pk=1)
        ChangeThresholdRule(watched_stock=watched_stock, when="A", percentage_threshold=50).full_clean()
        ChangeThresholdRule(watched_stock=watched_stock, when="B", percentage_threshold=50).full_clean()
        ChangeThresholdRule(watched_stock=watched_stock, when="O", percentage_threshold=50).full_clean()
        ChangeThresholdRule(watched_stock=watched_stock, when="O", percentage_threshold=-50).full_clean()
        ChangeThresholdRule(watched_stock=watched_stock, when="O", percentage_threshold=-50).full_clean()
        self.assertRaises(ValidationError, ChangeThresholdRule(watched_stock=watched_stock, when="D",
                                                               percentage_threshold=-50).full_clean)
        self.assertRaises(ValidationError, ChangeThresholdRule(watched_stock=watched_stock, when="O",
                                                               percentage_threshold=-101).full_clean)
        self.assertRaises(ValidationError, ChangeThresholdRule(watched_stock=watched_stock, when="O",
                                                               percentage_threshold=-101).full_clean)

    def test_price_threshold_rule(self):
        watched_stock = WatchedStock.objects.get(pk=1)
        PriceThresholdRule(watched_stock=watched_stock, when="A", price_threshold=50).full_clean()
        PriceThresholdRule(watched_stock=watched_stock, when="B", price_threshold=50).full_clean()
        PriceThresholdRule(watched_stock=watched_stock, when="O", price_threshold=50).full_clean()
        self.assertRaises(ValidationError, PriceThresholdRule(watched_stock=watched_stock, when="D",
                                                              price_threshold=50).full_clean)

    def test_recommendation_analyst_rule(self):
        watched_stock = WatchedStock.objects.get(pk=1)
        RecommendationAnalystRule(watched_stock=watched_stock, category="B").full_clean()
        RecommendationAnalystRule(watched_stock=watched_stock, category="MB").full_clean()
        RecommendationAnalystRule(watched_stock=watched_stock, category="MS").full_clean()
        RecommendationAnalystRule(watched_stock=watched_stock, category="H").full_clean()
        RecommendationAnalystRule(watched_stock=watched_stock, category="S").full_clean()
        self.assertRaises(ValidationError, RecommendationAnalystRule(watched_stock=watched_stock, category="D",
                                                                     ).full_clean)
