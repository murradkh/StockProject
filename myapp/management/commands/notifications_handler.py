import time

from django.core.management.base import BaseCommand
from myapp.scheduler import scheduler


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        jobs = scheduler()
        jobs.start()
        jobs.wait_jobs()
