from apscheduler.schedulers.background import BackgroundScheduler
from .stock_api_update import stock_api_update


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(stock_api_update)
    scheduler.add_job(stock_api_update, 'interval', seconds=10)
    scheduler.start()
