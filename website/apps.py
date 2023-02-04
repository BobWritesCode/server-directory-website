from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self):
        from website import updater
        updater.start()
        from website import jobs
        jobs.daily_jobs()
