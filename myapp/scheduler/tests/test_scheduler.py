from ..scheduler import *
from django.test import TestCase
import datetime


class SchedulerJobsTestCase(TestCase):

    def test_scheduler_thread(self):
        sch = scheduler()
        sch.start()
        jobs = sch.get_running_jobs()
        self.assertEqual(len(jobs), 5)
        for job in jobs:
            if job.name == change_status_rule.__name__:
                self.assertEqual(job.trigger.interval, datetime.timedelta(minutes=CHANGE_STATUS_RULE_THREAD_INT))
            elif job.name == change_threshold_rule.__name__:
                self.assertEqual(job.trigger.interval, datetime.timedelta(minutes=CHANGE_THRESHOLD_RULE_THREAD_INT))
            elif job.name == price_threshold_rule.__name__:
                self.assertEqual(job.trigger.interval, datetime.timedelta(minutes=PRICE_THRESHOLD_RULE_THREAD_INT))
            elif job.name == recommendation_analyst_rule.__name__:
                self.assertEqual(job.trigger.interval,
                                 datetime.timedelta(minutes=RECOMMENDATION_ANALYST_RULE_THREAD_INT))
        sch.stop_all_jobs()
