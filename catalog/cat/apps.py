from django.apps import AppConfig

from cat.templatetags.filters import get_type


class CatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cat'
    def ready(self):
        from django.template import engines


