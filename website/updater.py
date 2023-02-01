from apscheduler.schedulers.background import BackgroundScheduler

from .jobs import clear_bumps

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(clear_bumps, 'cron', hour='0-23')
    scheduler.start()

