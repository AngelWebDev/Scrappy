from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from office.views import signup, InviteAcceptView

urlpatterns = [
    path('arrival/', include('arrival.urls')),
    path('payout/', include('payout.urls')),
    path('office/', include('office.urls')),
    path('admin/', admin.site.urls),
    path('create-account/<str:key>', signup, name='signup'),
    url(r'^invitations/accept-invite/(?P<key>\w+)/?$', InviteAcceptView.as_view(), name='accept-invite'),
    path('invitations/', include('invitations.urls', namespace='invitations')),
    path('', include('django.contrib.auth.urls')),
]
