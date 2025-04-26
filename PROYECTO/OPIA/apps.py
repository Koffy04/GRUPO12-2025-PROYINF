from django.apps import AppConfig


class OpiaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'OPIA'

    def ready(self):
        import OPIA.signals

