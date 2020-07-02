from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ProductConfig(AppConfig):
    name = 'product_ventory.products'
    verbose_name = _("products")

    def ready(self):
        try:
            import product_ventory.products.signals  # noqa F401
        except ImportError:
            pass


