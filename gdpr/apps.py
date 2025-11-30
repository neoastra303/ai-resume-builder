from django.apps import AppConfig


class GdprConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gdpr"

    def ready(self):
        import gdpr.signals