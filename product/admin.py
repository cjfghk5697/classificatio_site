#Django admin 페이지에 Product 모델을 등록하는 코드
#admin.py
from django.contrib import admin
from .models import Product

admin.site.register(Product)