from django.core.management.base import BaseCommand
from myapp.scheduler import stock_api_update


# This class is Django's wy to implement managment commands
# You can run it with python manage.py stock_manager
# It will run 'handle' function
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        stock_api_update.stock_api_update()
