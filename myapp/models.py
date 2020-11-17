from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp import stock_api


# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=64)
    top_rank = models.IntegerField(null=True)
    price = models.FloatField()
    change = models.FloatField(null=True)
    change_percent = models.FloatField(null=True)
    market_cap = models.FloatField(null=True)
    primary_exchange = models.CharField(null=True, max_length=32)
    last_modified = models.DateTimeField(auto_now=True)

    @classmethod
    def add_to_watchlist(cls, profile, stock_symbol):
        stock = cls.objects.get(symbol=stock_symbol)
        profile.watchlist.add(stock)
        profile.save()

    @classmethod
    def remove_from_watchlist(cls, profile, stock_symbol):
        stock = cls.objects.get(symbol=stock_symbol)
        profile.watchlist.remove(stock)
        profile.save()

    @classmethod
    def add_to_db(cls, data):
        stock = cls.objects.create(symbol=data['symbol'],
                                   name=data['companyName'],
                                   # top_rank=None,
                                   price=data['latestPrice'],
                                   change=data['change'],
                                   change_percent=data['changePercent'],
                                   market_cap=data['marketCap'],
                                   primary_exchange=data['primaryExchange'])

    @classmethod
    def is_needed(cls, stock_symbol):
        stock = cls.objects.filter(symbol=stock_symbol)[:1]
        if not stock.exists():
            return False
        else:
            if stock[0].watchstock_set.all().count():
                return True
            else:
                return False


class WatchList:

    def __init__(self, profile):
        self.profile = profile

    def all(self):
        return list(map(lambda obj: obj.stock, WatchStock.objects.filter(profile=self.profile)))

    def add(self, stock):
        WatchStock.objects.create(profile=self.profile, stock=stock)

    def remove(self, stock):
        objects = WatchStock.objects.filter(profile=self.profile, stock=stock)
        for obj in objects:
            obj.delete()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # portfolio = models.ManyToManyField(Stock)

    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        self.watchlist = WatchList(self)

    def __str__(self):
        return f'{self.user.username}'


class WatchStock(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Notification(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    time = models.DateTimeField(auto_now=True)
    link = models.URLField(max_length=300, null=True)
    is_read = models.BooleanField(default=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications')
