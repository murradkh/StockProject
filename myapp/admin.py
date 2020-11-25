from django.contrib import admin
from .models import Stock, Profile, BoughtStock, SoldStock

admin.site.register(Stock)
admin.site.register(Profile)
admin.site.register(BoughtStock)
admin.site.register(SoldStock)