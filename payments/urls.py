# payments/urls.py

from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('pay/<str:tracking_number>/', views.pay_for_parcel_view, name='pay'),
]
