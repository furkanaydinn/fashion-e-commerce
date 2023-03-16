from django.urls import path
from .views import Shop,ProductDetail

urlpatterns = [
    path('shop/',Shop.as_view(),name='shop'),
    path('products/<int:id>/<str:category_slug>/<str:slug>/', ProductDetail.as_view(), name='product-detail'),
]


