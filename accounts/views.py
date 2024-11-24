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

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegistrationForm

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Ваш аккаунт було успішно створено! Ви можете увійти.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Будь ласка, виправте помилки у формі.')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})



from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomAuthenticationForm

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Ви успішно увійшли!')
            return redirect('accounts:profile')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.info(request, 'Ви вийшли з аккаунта.')
    return redirect('accounts:login')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профіль було оновлено.')
            return redirect('accounts:profile')
        else:
            # Відображення помилок форми
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from parcels.models import Parcel
from django.utils import timezone
import uuid

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user

        # Очищаємо дані користувача
        user.username = f'deleted_user_{uuid.uuid4()}'
        user.email = ''
        user.phone_number = ''
        user.is_active = False  # Деактивуємо акаунт
        user.set_unusable_password()  # Робимо пароль недійсним
        user.save()

        logout(request)  # Завершуємо сесію
        messages.success(request, 'Ваш обліковий запис було успішно видалено.')
        return redirect('accounts:home')  # Перенаправляємо на головну сторінку після видалення
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

    sent_parcels = sent_parcels.exclude(
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
from django.contrib.auth import get_user_model
from parcels.models import Parcel
from django.utils.timezone import now, timedelta

Pusser = get_user_model()

def home_view(request):
    # Отримання параметрів часу з GET-запиту
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Якщо дати не задані, встановлюємо проміжок за останні 7 днів
    if not start_date or not end_date:
        end_date = now()
        start_date = end_date - timedelta(days=7)

    # Перетворення дат з рядка в datetime
    try:
        start_date = now().strptime(start_date, '%Y-%m-%d')
        end_date = now().strptime(end_date, '%Y-%m-%d')
    except (TypeError, ValueError):
        # Якщо формат невірний, встановлюємо проміжок за останні 7 днів
        end_date = now()
        start_date = end_date - timedelta(days=7)

    # Обчислення нових користувачів і доставлених посилок
    new_users_count = Pusser.objects.filter(date_joined__range=(start_date, end_date)).count()
    delivered_parcels_count = Parcel.objects.filter(status='delivered', updated_at__range=(start_date, end_date)).count()
    parcels_count = Parcel.objects.filter(created_at__range=(start_date, end_date)).count()

    return render(request, 'accounts/home.html', {
        'new_users_count': new_users_count,
        'delivered_parcels_count': delivered_parcels_count,
        'parcels_count': parcels_count,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
    })