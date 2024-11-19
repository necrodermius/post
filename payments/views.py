from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from parcels.models import Parcel
from django.utils import timezone
from django.contrib import messages
from parcels.utils import calculate_distance, calculate_delivery_cost  # Імпортуємо наші функції
from .models import Payment  # Імпортуємо модель Payment
import uuid


@login_required
def pay_for_parcel_view(request, tracking_number):
    parcel = get_object_or_404(Parcel, tracking_number=tracking_number, recipient=request.user)
    if parcel.is_paid:
        messages.info(request, "Ця посилка вже оплачена.")
        return redirect('parcels:detail', tracking_number=tracking_number)

    # Розраховуємо відстань між адресами
    sender_address = parcel.sender_address  # Або отримуємо з parcel.sender.address
    recipient_address = parcel.recipient_address  # Або отримуємо з parcel.recipient.address

    distance = calculate_distance(sender_address, recipient_address)
    delivery_cost = calculate_delivery_cost(distance)

    if request.method == 'POST':
        # Імітація оплати
        parcel.is_paid = True
        parcel.paid_at = timezone.now()
        parcel.save()

        # Створюємо запис у моделі Payment
        payment = Payment.objects.create(
            user=request.user,
            amount=delivery_cost,
            payment_method='card',  # Або інший метод оплати
            status='completed',
            transaction_id=str(uuid.uuid4())  # Генеруємо унікальний ідентифікатор транзакції
        )

        messages.success(request, f"Посилка успішно оплачена. Ви можете її отримати. Сума оплати: {delivery_cost} грн.")
        return redirect('parcels:receive', tracking_number=tracking_number)

    return render(request, 'payments/pay_for_parcel.html', {
        'parcel': parcel,
        'delivery_cost': delivery_cost
    })
