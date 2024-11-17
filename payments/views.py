# payments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from parcels.models import Parcel
from django.utils import timezone
from django.contrib import messages
from parcels.tasks import hide_parcel

@login_required
def pay_for_parcel_view(request, tracking_number):
    parcel = get_object_or_404(Parcel, tracking_number=tracking_number, recipient=request.user)
    if parcel.is_paid:
        messages.info(request, "Ця посилка вже оплачена.")
        return redirect('parcels:detail', tracking_number=tracking_number)
    if request.method == 'POST':
        # Імітація оплати
        parcel.is_paid = True
        parcel.paid_at = timezone.now()
        parcel.save()
        messages.success(request, "Посилка успішно оплачена. Ви можете її отримати.")
        hide_parcel.apply_async((parcel.id,), countdown=3600)
        return redirect('parcels:receive', tracking_number=tracking_number)

    return render(request, 'payments/pay_for_parcel.html', {'parcel': parcel})


