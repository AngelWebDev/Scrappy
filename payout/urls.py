from django.urls import path

from . import views

urlpatterns = [
    path('', views.PayoutView.as_view(), name='payout_view'),
    path('open/<int:id>/', views.ArrivalPayoutRetrieveUpdateAPI.as_view(), name='payout_opened_detail'),
    path('open/', views.ArrivalPayoutListAPI.as_view(), name='payout_opened_list'),
    path('paid/', views.PayoutListAPI.as_view(), name='payout_paid_list'),
    path('paid/<int:id>/', views.PayoutDetailAPI.as_view(), name='payout_paid_detail'),
    path('report/', views.PayoutReportAPI.as_view(), name='payout_report'),
    path('reverse/<int:id>/', views.PayoutReversalAPI.as_view(), name='payout_reversal'),
]