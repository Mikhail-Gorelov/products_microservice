from django.apps import AppConfig


class ProductConfig(AppConfig):
    name = 'product'

    def ready(self) -> None:
        from api.v1.product import signals
