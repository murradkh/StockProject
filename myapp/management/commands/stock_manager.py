import time

from django.core.management.base import BaseCommand
from myapp.scheduler import stock_api_update

from myrails.settings import THREAD_INTERVAL


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        api = stock_api_update.stock_api_update
        while True:
            api()
            print('Stocks info updated\n')
            time.sleep(THREAD_INTERVAL)
