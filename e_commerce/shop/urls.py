from django.urls import path
from .views import ProductDetail

urlpatterns = [
    path('products/<int:id>/<str:category_slug>/<str:slug>/', ProductDetail.as_view(), name='product-detail'),
]