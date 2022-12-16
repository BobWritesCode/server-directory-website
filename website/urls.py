from django.urls import path

from website.views import ServerListings

urlpatterns = [
    path('', ServerListings.as_view(), name='home'),
]
