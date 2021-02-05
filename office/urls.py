from django.urls import path
from . import views

urlpatterns = [
    path('', views.OfficeView.as_view(), name='index'),
    path('user', views.UserUpdateDeleteAPI.as_view(), name='index'),
]