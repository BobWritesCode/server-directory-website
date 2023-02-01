from apscheduler.schedulers.background import BackgroundScheduler

from .jobs import clear_bumps

def start():
    scheduler = BackgroundScheduler()
    # add_job() Runs at midnight every night.
    scheduler.add_job(clear_bumps, 'cron', hour ='0')
    scheduler.start()

