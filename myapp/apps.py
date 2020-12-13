from django.apps import AppConfig
import sys


class MyappConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        # if 'django.core.wsgi' in sys.modules:
        #     return True
        from .scheduler import scheduler
        job = scheduler()
        job.start()
