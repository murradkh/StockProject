from django.apps import AppConfig
import sys

class MyappConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        # you must import your modules here
        # to avoid AppRegistryNotReady exception
        from .models import Stock
        from myapp import scheduler
        scheduler.start()