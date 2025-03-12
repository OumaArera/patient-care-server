from django.apps import AppConfig
import threading
from datetime import datetime
import pytz # type: ignore


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        if threading.current_thread().name != "MainThread":
            return

        from users.cron import start_scheduler
        start_scheduler()
