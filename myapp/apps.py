from django.apps import AppConfig
import sys


class MyappConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        from .scheduler import scheduler
        scheduler.start()
