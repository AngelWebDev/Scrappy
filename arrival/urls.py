from django.urls import path

from . import views

urlpatterns = [
    path('', views.ArrivalView.as_view(), name='arrival_view'),
    path('shipment', views.ArrivalCreateAPI.as_view(), name='shipment_api'),
    path('arrival_pos/<int:pk>', views.ArrivalPosDestroyAPI.as_view(), name='shipment_api'),
    path('material', views.MaterialAPI.as_view(), name='material_api'),
]