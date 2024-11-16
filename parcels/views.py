from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ParcelForm
from .models import Parcel
from .utils import generate_unique_tracking_number

@login_required
def create_parcel_view(request):
    if request.method == 'POST':
        form = ParcelForm(request.POST)
        if form.is_valid():
            parcel = form.save(sender=request.user)
            messages.success(request, f"Посилка успішно створена! Трек-номер: {parcel.tracking_number}")
            return redirect('parcels:detail', tracking_number=parcel.tracking_number)
    else:
        form = ParcelForm()
    return render(request, 'parcels/create_parcel.html', {'form': form})

def parcel_detail_view(request, tracking_number):
    parcel = get_object_or_404(Parcel, tracking_number=tracking_number)
    return render(request, 'parcels/parcel_detail.html', {'parcel': parcel})

# parcels/views.py

from .tasks import process_parcel

@login_required
def create_parcel_view(request):
    if request.method == 'POST':
        form = ParcelForm(request.POST)
        if form.is_valid():
            parcel = form.save(sender=request.user)
            messages.success(request, f"Посилка успішно створена! Трек-номер: {parcel.tracking_number}")
            # Викликаємо асинхронне завдання
            process_parcel.apply_async((parcel.id,), countdown=60)  # Через 1 хвилину
            return redirect('parcels:detail', tracking_number=parcel.tracking_number)
    else:
        form = ParcelForm()
    return render(request, 'parcels/create_parcel.html', {'form': form})

