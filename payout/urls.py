from django.urls import path

from . import views

urlpatterns = [
    path('', views.PayoutView.as_view(), name='payout_view'),
    path('arrived/<int:id>/', views.ArrivalPayoutRetrieveUpdateAPI.as_view(), name='payout_view'),
    path('arrived/', views.ArrivalPayoutListAPI.as_view(), name='payout_view'),
]