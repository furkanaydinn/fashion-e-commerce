from django.urls import path
from .views import ContactView,IndexView



urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('contact/', ContactView.as_view(), name='contact'),
]