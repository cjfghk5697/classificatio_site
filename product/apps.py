from django.apps import AppConfig
from .inference_code import PredictModel

class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'product'
    model=PredictModel()
    