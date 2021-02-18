from django.urls import path

from . import views

urlpatterns = [
    path('', views.PayoutView.as_view(), name='payout_view'),
]