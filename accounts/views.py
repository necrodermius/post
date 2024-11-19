# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from parcels.models import Parcel
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from payments.models import Payment

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш аккаунт було успішно створено! Ви можете увійти.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Ви успішно увійшли!')
            return redirect('accounts:profile')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Ви вийшли з аккаунта.')
    return redirect('accounts:login')

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профіль було оновлено.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        request.user.delete()  # Видаляємо користувача
        logout(request)        # Завершуємо сесію
        messages.success(request, 'Ваш обліковий запис було успішно видалено.')
        return redirect('main:index')  # Перенаправляємо на головну сторінку після видалення
    return render(request, 'accounts/delete_account.html')

# accounts/views.py


@login_required
def profile_view(request):
    user = request.user

    # Сортування
    sort_sent_by = request.GET.get('sort_sent_by', 'recipient__username')
    sort_received_by = request.GET.get('sort_received_by', 'sender__username')

    # Відправлені посилки
    sent_parcels = Parcel.objects.filter(sender=user).order_by(sort_sent_by)

    # Отримані посилки
    one_hour_ago = timezone.now() - timedelta(hours=1)

    received_parcels = Parcel.objects.filter(recipient=user).order_by(sort_received_by)

    # Виключаємо доставлені посилки, які були доставлені більше години тому
    received_parcels = received_parcels.exclude(
        status='delivered',
        is_received=True,
        updated_at__lte=one_hour_ago
    )

    payments = Payment.objects.filter(user=request.user)

    return render(request, 'accounts/profile.html', {
        'user': user,
        'sent_parcels': sent_parcels,
        'received_parcels': received_parcels,
        'sort_sent_by': sort_sent_by,
        'sort_received_by': sort_received_by,
        'payments': payments,
    })

from django.shortcuts import render
from django.contrib.auth.models import User
from parcels.models import Parcel  # Імпортуємо модель Parcel

from django.contrib.auth import get_user_model
Pusser = get_user_model()
def home_view(request):
    # Отримуємо кількість користувачів
    user_count = Pusser.objects.count()

    # Отримуємо загальну кількість посилок
    parcel_count = Parcel.objects.count()

    # Отримуємо кількість посилок, що доставляються (наприклад, зі статусом 'in_transit')
    delivering_parcels_count = Parcel.objects.filter(status='in_transit').count()

    return render(request, 'accounts/home.html', {
        'user_count': user_count,
        'parcel_count': parcel_count,
        'delivering_parcels_count': delivering_parcels_count,
    })