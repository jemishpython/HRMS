from django.apps import AppConfig


class HrmsApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hrms_api"

    def ready(self):
        import hrms_api.signals