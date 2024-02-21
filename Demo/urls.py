from django.urls import path
from Demo import views

urlpatterns = [
    path('', views.home, name='start'),
    path('redirect', views.redirect, name='redirect'),
    path('result', views.paidResult, name='result'),
    path('ipn', views.ipn, name='ipn')
]