''' website.apps.py '''

from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    '''Some default app settings and initialise cron jobs.'''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self):
        from website import updater
        from website import jobs
        updater.start()
        jobs.daily_jobs()
