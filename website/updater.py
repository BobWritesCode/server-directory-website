from apscheduler.schedulers.background import BackgroundScheduler

from .jobs import daily_jobs

def start():
    scheduler = BackgroundScheduler()
    # add_job() Runs at midnight every night.
    scheduler.add_job(daily_jobs, 'cron', hour ='0')
    scheduler.start()

