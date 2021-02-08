from django.urls import path
from . import views

urlpatterns = [
    path('', views.OfficeView.as_view(), name='office_view'),
    path('user', views.UserUpdateDeleteAPI.as_view(), name='user_api'),
    path('customer', views.CustomerAPIView.as_view(), name='customer_api'),
]