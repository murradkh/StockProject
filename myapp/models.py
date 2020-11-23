from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp import stock_api

# Create your models here.
from myapp.exceptions.stock_service import InvalidSellQuantityValue


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
    portfolio = models.OneToOneField("Portfolio", on_delete=models.CASCADE, null=True, related_name="profile")

    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)
        self.watchlist = WatchList(self)

    def __str__(self):
        return f'{self.user.username}'


class Portfolio(models.Model):
    budget = models.FloatField(default=500)

    def buy_stock(self, symbol, quantity=1):
        if quantity > 0:
            stock = Stock.objects.get(symbol=symbol)
            amount = quantity * stock.price
            BoughtStock.objects.create(portfolio=self, symbol=symbol, name=stock.name, quantity=quantity,
                                       expense_price=amount,
                                       budget_left=(self.budget - amount))
            self.budget -= amount
            self.save()
        else:
            raise InvalidSellQuantityValue("the amount of bought stocks is less than requested stocks to sell!")

    def sell_stock(self, symbol, quantity=1):
        bought_stocks = self.bought_stocks.filter(symbol=symbol, sold=False)
        if len(bought_stocks) >= quantity > 0:
            for bought_stock in bought_stocks[:quantity]:
                # SellStock.objects.create(portfolio=self, bought_stock=bought_stock, quantity=quantity, earning_price=, )
                pass
        else:
            raise InvalidSellQuantityValue("the amount of bought stocks is less than requested stocks to sell!")
        # stock = Stock.objects.get(symbol=symbol)
        # amount = quantity * stock.price
        # SellStock.objects.create(portfolio=self, symbol=symbol, name=stock.name, quantity=quantity,
        #                          expense_price=amount,
        #                          budget_left=(self.budget - amount))
        # self.budget -= amount
        # self.save()


class BoughtStock(models.Model):
    symbol = models.CharField(max_length=12)
    name = models.CharField(max_length=64)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="bought_stocks")
    created_on = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    expense_price = models.FloatField()
    budget_left = models.FloatField()
    sold = models.BooleanField(default=False)


class SoldStock(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="sold_stocks")
    bought_stock = models.ForeignKey(BoughtStock, on_delete=models.CASCADE, related_name="sold_stock")
    created_on = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)
    earning_price = models.FloatField()  # the price of which the <quantity> stocks sold
    budget_left = models.FloatField()
    gain_price = models.FloatField()  # its the profits gained from selling the stocks, which equals to
    # <earning-price> - <bought-price>


class WatchStock(models.Model):
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)
    stock = models.ForeignKey('Stock', on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, portfolio=Portfolio.objects.create())


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/
