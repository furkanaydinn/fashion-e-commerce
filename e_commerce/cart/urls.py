from django.urls import path
from .views import ShopCartView,OrderView


urlpatterns = [
    path('shopcart/', ShopCartView.as_view(), name='shopcart'),
    path('order/', OrderView.as_view(), name='order'),
]