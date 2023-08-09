from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .signals.tasks.post_migrate_signal import postMigrateSignalHandler


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        # Signal to load 31 days, 12 months and current year +10 -10 in database
        post_migrate.connect(postMigrateSignalHandler, sender=self)