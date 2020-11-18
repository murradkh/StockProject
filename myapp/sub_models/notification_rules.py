from django.db import models


class ChangeStatus(models.Model):
    """ status change rule is about notifying when a positive/negative change for sequential X days """
    watched_stock = models.ForeignKey("WatchedStock", on_delete=models.CASCADE, related_name='change_status_rules')
    status = models.CharField(max_length=10, choices=[('N', 'Negative'), ('P', 'Positive')], default='P')
    num_of_days = models.PositiveIntegerField(default=30)


class ChangeThreshold(models.Model):
    """ change threshold rule is about notifying when the change of stock reaching a specific threshold percentage """
    watched_stock = models.ForeignKey("WatchedStock", on_delete=models.CASCADE, related_name='change_threshold_rules')


class PriceThreshold(models.Model):
    """ price threshold rule is about notifying when the price of stock reaching a specific threshold value """
    watched_stock = models.ForeignKey("WatchedStock", on_delete=models.CASCADE, related_name='price_threshold_rules')


class ActivityPeriod(models.Model):
    """ activity rule is about notifying when a period of days the stock was in top_ranks/mostActive stocks"""
    watched_stock = models.ForeignKey("WatchedStock", on_delete=models.CASCADE, related_name='activity_period_rules')


class RecommendationAnalyst(models.Model):
    """ Recommendation-Analyst rule is about notifying when the stock recommended to
    Buy/Over-Weight/Hold/Under-Weight/Sell"""
    watched_stock = models.ForeignKey("WatchedStock", on_delete=models.CASCADE,
                                      related_name='recommendation_analyst_rules')
