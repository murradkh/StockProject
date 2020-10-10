from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Stock(models.Model):
	symbol = models.CharField(max_length=12, primary_key=True)
	name = models.CharField(max_length=64)
	top_rank = models.IntegerField(null=True)
	price = models.FloatField()
	change = models.FloatField(null=True)
	change_percent = models.FloatField()
	market_cap = models.FloatField(null=True)
	primary_exchange = models.CharField(null=True, max_length=32)

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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    watchlist = models.ManyToManyField(Stock)
    # portfolio = models.ManyToManyField(Stock)

    def __str__(self):
        return f'{self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/