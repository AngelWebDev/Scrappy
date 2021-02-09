from django.contrib import admin
from django.urls import include, path
from office.views import signup

urlpatterns = [
    path('arrival/', include('arrival.urls')),
    path('payout/', include('payout.urls')),
    path('office/', include('office.urls')),
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('', include('django.contrib.auth.urls')),
]
