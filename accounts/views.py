# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from parcels.models import Parcel
from django.db.models import Q

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
    return redirect('accounts:register')

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
    # Отримуємо параметри сортування з GET-запиту
    sort_sent_by = request.GET.get('sort_sent_by', 'tracking_number')  # Значення за замовчуванням
    sort_received_by = request.GET.get('sort_received_by', 'tracking_number')

    # Список дозволених полів для сортування
    allowed_sort_fields_sent = ['recipient__username', 'description', 'weight', 'status', 'tracking_number']
    allowed_sort_fields_received = ['sender__username', 'description', 'weight', 'status', 'tracking_number']

    # Перевірка дозволених полів для відправлених посилок
    if sort_sent_by not in allowed_sort_fields_sent:
        sort_sent_by = 'tracking_number'

    # Перевірка дозволених полів для отриманих посилок
    if sort_received_by not in allowed_sort_fields_received:
        sort_received_by = 'tracking_number'

    # Отримуємо відсортовані посилки
    sent_parcels = Parcel.objects.filter(sender=request.user).order_by(sort_sent_by)
    received_parcels = Parcel.objects.filter(recipient=request.user).order_by(sort_received_by)

    return render(request, 'accounts/profile.html', {
        'sent_parcels': sent_parcels,
        'received_parcels': received_parcels,
        'sort_sent_by': sort_sent_by,
        'sort_received_by': sort_received_by,
    })






