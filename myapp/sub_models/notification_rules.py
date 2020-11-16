from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import QuerySet


class ChangeStatusRule(models.Model):
    """ status change rule is about notifying when a positive/negative change for sequential X days """

    watched_stock = models.ForeignKey("WatchedStock", on_delete=models.CASCADE, related_name='change_status_rules')
    status = models.CharField(max_length=10, choices=[('N', 'Negative'), ('P', 'Positive')], default='P')
    num_of_days = models.PositiveIntegerField(default=30, validators=[MaxValueValidator(360), MinValueValidator(2)])

    @classmethod
    def get_rules(cls) -> QuerySet:
        return ChangeStatusRule.objects.all()


class ChangeThresholdRule(models.Model):
    """ change threshold rule is about notifying when the change of stock reaching a specific threshold percentage """
    watched_stock = models.ForeignKey("WatchedStock", on_delete=models.CASCADE, related_name='change_threshold_rules')


class PriceThresholdRule(models.Model):
    """ price threshold rule is about notifying when the price of stock reaching a specific threshold value """
    watched_stock = models.ForeignKey("WatchedStock", on_delete=models.CASCADE, related_name='price_threshold_rules')


class ActivityPeriodRule(models.Model):
    """ activity rule is about notifying when a period of days the stock was in top_ranks/mostActive stocks"""
    watched_stock = models.ForeignKey("WatchedStock", on_delete=models.CASCADE, related_name='activity_period_rules')


class RecommendationAnalystRule(models.Model):
    """ Recommendation-Analyst rule is about notifying when the stock recommended to
    Buy/Over-Weight/Hold/Under-Weight/Sell"""
    watched_stock = models.ForeignKey("WatchedStock", on_delete=models.CASCADE,
                                      related_name='recommendation_analyst_rules')
