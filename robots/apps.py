from django.apps import AppConfig
from django.db.models.signals import pre_save


class RobotsConfig(AppConfig):
    name = 'robots'

    def ready(self):
        import robots.signals
