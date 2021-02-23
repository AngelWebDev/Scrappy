from django.urls import path

from . import views

urlpatterns = [
    path('', views.ArrivalView.as_view(), name='arrival_view'),
    path('shipment', views.ArrivalAPI.as_view(), name='shipment_api'),
    path('material', views.MaterialAPI.as_view(), name='material_api'),
]