
from django.apps import AppConfig


class UploadsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uploads'

#when we run the program it first checks if there is any file to remove
    def ready(self):
        import threading
        from .cleanup import delete_expired_files
        threading.Timer(1.0, delete_expired_files).start()