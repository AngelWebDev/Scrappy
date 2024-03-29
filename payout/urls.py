from django.urls import path

from . import views

urlpatterns = [
    path('', views.PayoutView.as_view(), name='payout_view'),
    path('open/<int:id>/', views.ArrivalPayoutRetrieveUpdateAPI.as_view(), name='payout_opened_detail'),
    path('open/<int:id>/<int:customer_id>/', views.ArrivalChangeCustomerAPI.as_view(), name='arrival_change_customer'),
    path('open/', views.ArrivalPayoutListAPI.as_view(), name='payout_opened_list'),
    path('paid/', views.PayoutListAPI.as_view(), name='payout_paid_list'),
    path('paid/<int:id>/', views.PayoutDetailAPI.as_view(), name='payout_paid_detail'),
    path('report/', views.PayoutReportAPI.as_view(), name='payout_report'),
    path('reverse/<int:id>/', views.PayoutReversalAPI.as_view(), name='payout_reversal'),
    path('report/email/', views.PayoutReportEmailAPI.as_view(), name='payout_report_email'),
]