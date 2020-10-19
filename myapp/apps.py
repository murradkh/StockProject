from django.apps import AppConfig


class MyappConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        from .scheduler import scheduler
        scheduler.start()
