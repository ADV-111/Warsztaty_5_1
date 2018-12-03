from django.apps import AppConfig


class CwirekConfig(AppConfig):
    name = 'cwirek'

    def ready(self):
        import cwirek.signals
