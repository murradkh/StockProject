from django.db import models


class WatchedStockRule(models.Model):
    change_status = models.OneToOneField("ChangeStatus", on_delete=models.CASCADE,
                                         related_name='watched_stock_rule')
    change_threshold = models.OneToOneField("ChangeThreshold", on_delete=models.CASCADE,
                                            related_name='watched_stock_rule')
    price_threshold = models.OneToOneField("PriceThreshold", on_delete=models.CASCADE,
                                           related_name='watched_stock_rule')
    activity = models.OneToOneField("Activity", on_delete=models.CASCADE,
                                    related_name='watched_stock_rule')


class ChangeStatus(models.Model):
    pass


class ChangeThreshold(models.Model):
    pass


class PriceThreshold(models.Model):
    pass


class Activity(models.Model):
    pass
