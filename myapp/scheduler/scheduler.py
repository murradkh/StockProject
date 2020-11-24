from apscheduler.schedulers.background import BackgroundScheduler

from .notification_rules_handler import change_status_rule, \
    change_threshold_rule, price_threshold_rule, recommendation_analyst_rule
from .stock_api_update import stock_api_update
from myrails.settings import THREAD_INTERVAL

CHANGE_STATUS_RULE_THREAD_INT = 1  # one minute interval
CHANGE_THRESHOLD_RULE_THREAD_INT = 1  # one minute interval
PRICE_THRESHOLD_RULE_THREAD_INT = 1  # one minute interval
RECOMMENDATION_ANALYST_RULE_THREAD_INT = 1  # one minute interval


class scheduler:
    def __init__(self):
        self.scheduler_job = BackgroundScheduler()
        self.scheduler_job.add_job(stock_api_update, 'interval',
                                   seconds=THREAD_INTERVAL)
        self.scheduler_job.add_job(change_status_rule, 'interval', minutes=CHANGE_STATUS_RULE_THREAD_INT,
                                   max_instances=1)
        self.scheduler_job.add_job(change_threshold_rule, 'interval', minutes=CHANGE_THRESHOLD_RULE_THREAD_INT,
                                   max_instances=1)
        self.scheduler_job.add_job(price_threshold_rule, 'interval', minutes=PRICE_THRESHOLD_RULE_THREAD_INT,
                                   max_instances=1)
        self.scheduler_job.add_job(recommendation_analyst_rule, 'interval',
                                   minutes=RECOMMENDATION_ANALYST_RULE_THREAD_INT, max_instances=1)

    def start(self):
        self.scheduler_job.start()

    def stop_all_jobs(self):
        # Removes all jobs from this store.
        self.scheduler_job.remove_all_jobs()
        # Frees any resources still bound to this job store.
        self.scheduler_job.shutdown()

    def get_running_jobs(self):
        return self.scheduler_job.get_jobs()
