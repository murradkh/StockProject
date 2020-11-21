from ..scheduler import scheduler
import threading
from django.test import TestCase


class SchedulerJobsTestCase(TestCase):

    def test_scheduler_thread(self):
        one = threading.active_count()
        job = scheduler()
        job.start()
        self.assertNotEqual(one, threading.active_count())
        job.stop_all_jobs()
