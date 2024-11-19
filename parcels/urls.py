from django.urls import path
from . import views

app_name = 'parcels'

urlpatterns = [
    path('create/', views.create_parcel_view, name='create'),
    path('detail/<str:tracking_number>/', views.parcel_detail_view, name='detail'),
    path('redirect/<str:tracking_number>/', views.redirect_parcel_view, name='redirect'),
    path('edit/<str:tracking_number>/', views.edit_parcel_view, name='edit'),
    path('receive/<str:tracking_number>/', views.receive_parcel_view, name='receive'),

    # Інші маршрути
]
