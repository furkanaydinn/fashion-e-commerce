from django.urls import path
from .views import BlogList,BlogDetail

urlpatterns = [
    path('blog/', BlogList.as_view(), name='login'),
    path('blog/<slug:slug>/', BlogDetail.as_view(), name='blog-detail'),
]
