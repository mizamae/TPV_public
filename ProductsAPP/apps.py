from django.apps import AppConfig
import logging
logger = logging.getLogger("models")


class ProductsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ProductsAPP'

    def ready(self):
        pass

