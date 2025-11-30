from django.urls import path
from . import views

urlpatterns = [
    path('setup/', views.two_factor_setup, name='two_factor_setup'),
    path('verify/', views.two_factor_verify, name='two_factor_verify'),
    path('dashboard/', views.two_factor_dashboard, name='two_factor_dashboard'),
    path('disable/<int:device_id>/', views.two_factor_disable, name='two_factor_disable'),
]