from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('server-list/<slug>', views.ServerListings.as_view(), name='server-list'),
    path('server/<slug>', views.ServerDetail.as_view(), name='server'),
    path('login/', views.login, name='login'),
]
