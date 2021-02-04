from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserListCreateView.as_view(), name='index'),
    path('<int:id>/update', views.UserUpdateView.as_view(), name='update_user'),
]