from django.urls import path
from . import views

urlpatterns = [
    path('', views.gdpr_dashboard, name='gdpr_dashboard'),
    path('request-deletion/', views.request_data_deletion, name='request_data_deletion'),
    path('cancel-deletion/<int:request_id>/', views.cancel_data_deletion, name='cancel_data_deletion'),
    path('request-access/', views.request_data_access, name='request_data_access'),
]