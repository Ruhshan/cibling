from django.apps import AppConfig


class CiblingWebConfig(AppConfig):
    name = 'cibling_web'

    def ready(self):
        import cibling_web.signals
