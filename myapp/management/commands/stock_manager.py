import time

from django.core.management.base import BaseCommand
from myapp.scheduler import stock_api_update

# This class is Django's wy to implement managment commands
# You can run it with python manage.py stock_manager
# It will run 'handle' function
from myrails.settings import THREAD_INTERVAL
import logging


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        api = stock_api_update.stock_api_update
        while True:
            api()
            logging.info('Stocks info updated')
            time.sleep(THREAD_INTERVAL)
