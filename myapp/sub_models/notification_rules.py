from django.db import models


class Rules(models.Model):
    pass


class ChangeStatus(models.Model):
    rules = models.ForeignKey(Rules, on_delete=models.CASCADE, related_name='change_statuses', null=True)
    # positive_change = models.


class ChangeThreshold(models.Model):
    rules = models.ForeignKey(Rules, on_delete=models.CASCADE, related_name='change_thresholds', null=True)


class PriceThreshold(models.Model):
    rules = models.ForeignKey(Rules, on_delete=models.CASCADE, related_name='price_thresholds', null=True)


class Activity(models.Model):
    rules = models.ForeignKey(Rules, on_delete=models.CASCADE, related_name='activity', null=True)
