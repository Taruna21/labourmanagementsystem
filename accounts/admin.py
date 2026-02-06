from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_available")
    list_filter = ("is_available",)
    search_fields = ("user__username", "user__email")
