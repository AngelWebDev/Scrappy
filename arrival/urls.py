from django.urls import path

from . import views

urlpatterns = [
    path('', views.ArrivalView.as_view(), name='arrival_view'),
    path('material', views.ArrivalAPI.as_view(), name='material_api'),
]