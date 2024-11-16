from django.shortcuts import render

# Create your views here.
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from parcels.models import Parcel

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
def profile_view(request):
    return render(request, 'accounts/profile.html')

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


@login_required
def profile_view(request):
    sent_parcels = Parcel.objects.filter(sender=request.user)
    received_parcels = Parcel.objects.filter(recipient=request.user)
    return render(request, 'accounts/profile.html', {
        'sent_parcels': sent_parcels,
        'received_parcels': received_parcels
    })






