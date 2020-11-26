from django.contrib import admin
from .models import Stock, Profile, SoldStock, BoughtStock, Portfolio

admin.site.register(Stock)
admin.site.register(Profile)
admin.site.register(SoldStock)
admin.site.register(BoughtStock)
admin.site.register(Portfolio)
