from django.urls import path
from . import views

urlpatterns = [
    path('', views.OfficeView.as_view(), name='office_view'),
    path('user/', views.UserAPI.as_view(), name='user_api'),
    path('user/invite/', views.UserInviteAPI.as_view(), name='user_invite'),
    path('customer/', views.CustomerAPIView.as_view(), name='customer_api'),
    path('identification/', views.IdentificationCreateAPI.as_view(), name='id_create'),
]