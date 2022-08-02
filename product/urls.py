from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

urlpatterns=[
    path('product/<int:pk>/',views.ProductPredictAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
