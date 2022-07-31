#/djangoProject/url.py
from django.contrib import admin
from django.urls import path
from product.views import ProductListAPI,ProductDetailAPI
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url, include
from rest_framework import routers
from product import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductListAPI)

urlpatterns = [
    url(r'^', include(router.urls)),
    path('admin/', admin.site.urls),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
   	url(r'^api-auth/<int:pk>', ProductDetailAPI.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)