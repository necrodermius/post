from django.urls import path
from . import views

app_name = 'parcels'

urlpatterns = [
    path('create/', views.create_parcel_view, name='create'),
    path('detail/<str:tracking_number>/', views.parcel_detail_view, name='detail'),
    # Інші маршрути
]
