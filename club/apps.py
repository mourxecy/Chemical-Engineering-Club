# club/apps.py
from django.apps import AppConfig

class ClubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'club'

    def ready(self):
        import club.signals  # noqa: F401

