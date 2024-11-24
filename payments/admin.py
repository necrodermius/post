from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'parcel', 'amount', 'payment_method', 'status', 'timestamp')
    list_filter = ('payment_method', 'status', 'timestamp')
    search_fields = ('user__username', 'parcel__tracking_number', 'transaction_id')

admin.site.register(Payment, PaymentAdmin)
