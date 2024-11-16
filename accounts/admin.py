from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "phone_number")
    search_fields = ("id", "first_name", "last_name", "email", "phone_number")
