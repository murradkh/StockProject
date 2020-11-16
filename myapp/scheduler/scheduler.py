from apscheduler.schedulers.background import BackgroundScheduler

from .notification_updater import change_status_rule, CHANGE_STATUS_RULE_THREAD_INTERVAL
from .stock_api_update import stock_api_update
from myrails.settings import THREAD_INTERVAL


class scheduler:
    def __init__(self):
        self.scheduler_job = BackgroundScheduler()
        self.scheduler_job.add_job(stock_api_update)
        self.scheduler_job.add_job(stock_api_update, 'interval',
                                   seconds=THREAD_INTERVAL)
        self.scheduler_job.add_job(change_status_rule, 'interval', seconds=CHANGE_STATUS_RULE_THREAD_INTERVAL)

    def start(self):
        self.scheduler_job.start()

    def stop_all_jobs(self):
        # Removes all jobs from this store.
        self.scheduler_job.remove_all_jobs()
        # Frees any resources still bound to this job store.
        self.scheduler_job.shutdown()

    def get_running_jobs(self):
        return self.scheduler_job.get_jobs()
