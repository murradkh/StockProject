from apscheduler.schedulers.background import BackgroundScheduler
from .stock_api_update import stock_api_update


class scheduler:
    def __init__(self):
        self.scheduler_job = BackgroundScheduler()
        self.scheduler_job.add_job(stock_api_update)
        self.scheduler_job.add_job(stock_api_update, 'interval', seconds=10)

    def start(self):
        self.scheduler_job.start()

    def stop_all_jobs(self):
        # Removes all jobs from this store.
        self.scheduler_job.remove_all_jobs()
        # Frees any resources still bound to this job store.
        self.scheduler_job.shutdown()

    def get_running_jobs(self):
        return self.scheduler_job.get_jobs()
