from django.contrib import admin
from .models import Stock, Profile, Notification

admin.site.register(Stock)
admin.site.register(Profile)
admin.site.register(Notification)
