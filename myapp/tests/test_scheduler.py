from ..scheduler import scheduler
import threading
from django.test import TestCase
from ..scheduler.stock_api_update import stock_api_update
from ..models import Stock


class SchedulerJobsTestCase(TestCase):

    def test_scheduler_thread(self):
        one = threading.active_count()
        job = scheduler()
        job.start()
        self.assertNotEqual(one, threading.active_count())
        job.stop_all_jobs()


class JbsTestCase(TestCase):

    def test_api_update(self):
        stock_api_update()
        value_1 = Stock.objects.filter(top_rank=1)[0].last_modified
        stock_api_update()
        value_2 = Stock.objects.filter(top_rank=1)[0].last_modified
        self.assertNotEqual(value_1, value_2)


#TODO: test the jobs here