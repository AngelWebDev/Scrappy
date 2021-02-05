from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('arrival', include('arrival.urls')),
    path('payout', include('payout.urls')),
    path('office', include('office.urls')),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
]
