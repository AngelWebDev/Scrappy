from django.urls import path

from . import views

urlpatterns = [
    path('', views.ArrivalView.as_view(), name='index'),
]