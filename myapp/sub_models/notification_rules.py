from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import QuerySet


class ChangeStatusRule(models.Model):
    """ status change rule is about notifying when a positive/negative change for sequential X days """

    watched_stock = models.ForeignKey("WatchedStock", on_delete=models.CASCADE, related_name='change_status_rules')
    status = models.CharField(max_length=10, choices=[('N', 'Negative'), ('P', 'Positive')], default='P')
    num_of_days = models.PositiveIntegerField(default=30, validators=[MaxValueValidator(360), MinValueValidator(2)])
    fired = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.num_of_days} sequential days'

    @classmethod
    def get_rules(cls) -> QuerySet:
        return ChangeStatusRule.objects.all()


class ChangeThresholdRule(models.Model):
    """ change value rule is about notifying when the change of stock reaching a specific change value percentage """
    watched_stock = models.ForeignKey("WatchedStock", on_delete=models.CASCADE, related_name='change_threshold_rules')
    when = models.CharField(max_length=20, choices=[('B', 'Below threshold'), ('A', 'Above threshold'),
                                                    ('O', 'On threshold')], default='A')
    percentage_threshold = models.FloatField(default=0, validators=[MaxValueValidator(100), MinValueValidator(
        -100)])
    fired = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.percentage_threshold} percentage threshold'

    @classmethod
    def get_rules(cls) -> QuerySet:
        return ChangeThresholdRule.objects.all()


class PriceThresholdRule(models.Model):
    """ price threshold rule is about notifying when the price of stock reaching a specific threshold value """
    watched_stock = models.ForeignKey("WatchedStock", on_delete=models.CASCADE, related_name='price_threshold_rules')
    when = models.CharField(max_length=20, choices=[('B', 'Below threshold'), ('A', 'Above threshold'),
                                                    ('O', 'On threshold')], default='A')
    price_threshold = models.FloatField(default=0)
    fired = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.price_threshold} price threshold'

    @classmethod
    def get_rules(cls) -> QuerySet:
        return PriceThresholdRule.objects.all()


class RecommendationAnalystRule(models.Model):
    """ Recommendation-Analyst rule is about notifying when the stock recommended to
    Buy/Over-Weight/Hold/Under-Weight/Sell"""
    watched_stock = models.ForeignKey("WatchedStock", on_delete=models.CASCADE,
                                      related_name='recommendation_analyst_rules')
    category = models.CharField(max_length=20, choices=[('B', 'Buy'), ('MB', 'Moderate Buy'),
                                                        ('H', 'Hold'), ("MS", "Moderate Sell"), ("S", "Sell")],
                                default='B')
    threshold_recommenders_percentage = models.FloatField(default=0, validators=[MaxValueValidator(100),
                                                                                 MinValueValidator(1)])
    fired = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.watched_stock.stock.name}'

    @classmethod
    def get_rules(cls) -> QuerySet:
        return RecommendationAnalystRule.objects.all()
