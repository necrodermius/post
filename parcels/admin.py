from django.contrib import admin
from .models import Parcel

@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = (
        'tracking_number',
        'sender',
        'recipient',
        'status',
        'created_at',
        'updated_at',
        'is_paid',
        'is_received',
    )
    list_filter = (
        'status',
        'is_paid',
        'is_received',
        'redirected',
        'custom_address',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'tracking_number',
        'sender__username',
        'sender__email',
        'sender__phone_number',
        'recipient__username',
        'recipient__email',
        'recipient__phone_number',
    )
    readonly_fields = ('created_at', 'updated_at', 'sender_address_display', 'recipient_address_display')
    fieldsets = (
        (None, {
            'fields': ('tracking_number', 'sender', 'recipient', 'status', 'description', 'weight')
        }),
        ('Адреси', {
            'fields': ('sender_address_display', 'recipient_address_display', 'redirect_address', 'custom_recipient_address')
        }),
        ('Додаткова інформація', {
            'fields': ('redirected', 'custom_address', 'current_location', 'is_paid', 'paid_at', 'is_received', 'hidden_at')
        }),
    )
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def sender_address_display(self, obj):
        return obj.sender_address()
    sender_address_display.short_description = 'Адреса відправника'

    def recipient_address_display(self, obj):
        return obj.recipient_address()
    recipient_address_display.short_description = 'Адреса отримувача'
