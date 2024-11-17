
from .forms import ParcelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Parcel
from .forms import RedirectParcelForm
from .tasks import process_redirected_parcel

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

@login_required
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

@login_required
def redirect_parcel_view(request, tracking_number):
    parcel = get_object_or_404(Parcel, tracking_number=tracking_number, recipient=request.user)

    if request.method == 'POST':
        form = RedirectParcelForm(request.POST, instance=parcel)
        if form.is_valid():
            parcel = form.save(commit=False)
            parcel.redirected = True
            parcel.save()
            messages.success(request, f"Посилка {parcel.tracking_number} була успішно переадресована.")
            # Запускаємо завдання Celery для обробки переадресації
            process_redirected_parcel.delay(parcel.id)
            return redirect('parcels:detail', tracking_number=parcel.tracking_number)
    else:
        form = RedirectParcelForm(instance=parcel)
    return render(request, 'parcels/redirect_parcel.html', {'form': form, 'parcel': parcel})

@login_required
def edit_parcel_view(request, tracking_number):
    parcel = get_object_or_404(Parcel, tracking_number=tracking_number, sender=request.user)
    if request.method == 'POST':
        form = ParcelForm(request.POST, instance=parcel)
        if form.is_valid():
            form.save()
            messages.success(request, "Посилка успішно оновлена.")
            return redirect('parcels:detail', tracking_number=parcel.tracking_number)
    else:
        form = ParcelForm(instance=parcel)
    return render(request, 'parcels/edit_parcel.html', {'form': form, 'parcel': parcel})