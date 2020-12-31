import threading

from apscheduler.schedulers.background import BackgroundScheduler

from .notification_rules_handler import change_status_rule, \
    change_threshold_rule, price_threshold_rule, recommendation_analyst_rule
from .stock_api_update import stock_api_update


class scheduler:
    def __init__(self):
        self.jobs = []
        self.jobs.append(threading.Thread(target=change_status_rule, args=(True,)))
        self.jobs.append(threading.Thread(target=change_threshold_rule, args=(True,)))
        self.jobs.append(threading.Thread(target=price_threshold_rule, args=(True,)))
        self.jobs.append(threading.Thread(target=recommendation_analyst_rule, args=(True,)))

    def start(self):
        for job in self.jobs:
            job.start()

    def wait_jobs(self):
        for job in self.jobs:
            job.join()
