from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('server-list/<slug>', views.ServerListings.as_view(), name='server-list'),
]
