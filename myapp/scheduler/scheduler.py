from apscheduler.schedulers.background import BackgroundScheduler
from .stock_api_update import stock_api_update


class scheduler:
    def __init__(self):
        self.scheduler_job = BackgroundScheduler()
        self.scheduler_job.add_job(stock_api_update)
        self.scheduler_job.add_job(stock_api_update, 'interval', seconds=10)

    def start(self):
        self.scheduler_job.start()

    def stop(self):
        self.scheduler_job.remove_all_jobs()
    def get_running_jobs(self):
        return self.scheduler_job.get_jobs()
