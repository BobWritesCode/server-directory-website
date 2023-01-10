from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('server-list/<slug>', views.ServerListings.as_view(), name='server-list'),
    path('server/<slug>', views.ServerDetail.as_view(), name='server'),
    path('accounts/login', views.login, name='login'),
    path('accounts/signup', views.SignUpView.as_view(), name='signup'),
    path('accounts/myaccount', views.myaccount, name='my-account'),
]
