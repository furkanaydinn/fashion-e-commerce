from django.urls import path
from .views import ContactView,IndexView

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),
    path('',IndexView.as_view(),name='index'),
]