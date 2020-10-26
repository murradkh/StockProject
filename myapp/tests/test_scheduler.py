from django.test import TestCase
from ..scheduler import scheduler
import threading



class test_scheduler(TestCase):

    def test_scheduler_thread(self):
        one = threading.active_count()
        job = scheduler()
        job.start()
        self.assertNotEqual(one, threading.active_count())
        job.stop()


