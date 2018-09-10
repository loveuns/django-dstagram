from django.apps import AppConfig


class PhotoConfig(AppConfig):
    name = 'photo'

    def ready(self):
        from . import signals