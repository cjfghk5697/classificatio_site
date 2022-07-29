#/djangoProject/url.py
from django.contrib import admin
from django.urls import path
from product.views import ProductListAPI,ProductDetailAPI

urlpatterns = [
    path('admin/', admin.site.urls),
	path('api/product/', ProductListAPI.as_view()),
   	path('api/product/<int:pk>', ProductDetailAPI.as_view())

]