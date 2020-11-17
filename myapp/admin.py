from django.contrib import admin
from .models import Stock, Profile, Notification, WatchedStock
from .sub_models.notification_rules import ChangeStatusRule, ChangeThresholdRule

admin.site.register(Stock)
admin.site.register(Profile)
admin.site.register(Notification)
admin.site.register(WatchedStock)
admin.site.register(ChangeStatusRule)
admin.site.register(ChangeThresholdRule)
