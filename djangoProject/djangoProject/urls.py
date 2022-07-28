#/djangoProject/url.py
from django.contrib import admin
from django.urls import path
from product.views import ProductListAPI

urlpatterns = [
    path('admin/', admin.site.urls),
	path('api/product/', ProductListAPI.as_view())
]