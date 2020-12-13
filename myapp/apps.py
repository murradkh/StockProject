from django.apps import AppConfig
import os


class MyappConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        if not os.getenv('STOCK_PROJECT_MACHINE_TYPE'):
            return True
        from .scheduler import scheduler
        job = scheduler()
        job.start()
