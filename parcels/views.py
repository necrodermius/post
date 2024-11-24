
from .forms import ParcelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Parcel
from .forms import RedirectParcelForm
from .tasks import process_redirected_parcel


@login_required
def parcel_detail_view(request, tracking_number):
    parcel = get_object_or_404(Parcel, tracking_number=tracking_number)
    return render(request, 'parcels/parcel_detail.html', {'parcel': parcel})

# parcels/views.py

from .tasks import process_parcel

# parcels/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ParcelForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ParcelForm
from .tasks import process_parcel
from django.utils import timezone

@login_required
def create_parcel_view(request):
    user = request.user

    # Перевіряємо, чи всі обов'язкові поля профілю заповнені
    required_profile_fields = ['country', 'city', 'street', 'building', 'postal_code']
    missing_fields = [field for field in required_profile_fields if not getattr(user, field)]

    if missing_fields:
        messages.error(request, "Ви повинні заповнити свій профіль перед відправленням посилки.")
        return redirect('accounts:edit_profile')

    if request.method == 'POST':
        form = ParcelForm(request.POST)
        if form.is_valid():
            parcel = form.save(commit=False, sender=user)
            parcel.save()
            messages.success(request, "Посилка успішно створена.")
            # Запускаємо завдання для обробки посилки (якщо використовується Celery)
            process_parcel.apply_async((parcel.id,), countdown=60)
            return redirect('parcels:detail', tracking_number=parcel.tracking_number)
        else:
            # Відображення повідомлень про помилки форми
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = ParcelForm()
        form.initial['sender_id'] = user.id  # Передаємо ID відправника до форми

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


# parcels/views.py

@login_required
def receive_parcel_view(request, tracking_number):
    parcel = get_object_or_404(Parcel, tracking_number=tracking_number, recipient=request.user)
    if not parcel.is_paid:
        messages.error(request, "Ви повинні спочатку оплатити посилку.")
        return redirect('payments:pay', tracking_number=tracking_number)
    if parcel.is_received:
        messages.info(request, "Ви вже отримали цю посилку.")
        return redirect('parcels:detail', tracking_number=tracking_number)
    if request.method == 'POST':
        parcel.is_received = True
        parcel.status = 'delivered'
        parcel.save()
        messages.success(request, "Ви успішно отримали посилку.")
        return redirect('parcels:detail', tracking_number=tracking_number)
    return render(request, 'parcels/receive_parcel.html', {'parcel': parcel})

from django.shortcuts import render
from .models import Parcel


