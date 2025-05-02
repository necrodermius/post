from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "phone_number")
    search_fields = ("id", "first_name", "last_name", "email", "phone_number")

from django.contrib.admin.models import LogEntry
class LogEntryAdmin(admin.ModelAdmin):
    list_display = (
        "action_time", "content_type", "object_repr",
        "action_flag", "user", "change_message",
    )
    date_hierarchy = "action_time"
    search_fields = ("object_repr", "change_message")
    list_filter = ("action_flag", "content_type")

admin.site.register(LogEntry, LogEntryAdmin)

