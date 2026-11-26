from django.contrib import admin

from .models import Turf, TurfOwner


@admin.register(TurfOwner)
class TurfOwnerAdmin(admin.ModelAdmin):
    list_display = ("id", "business_name", "whatsapp_number", "user")
    search_fields = ("business_name", "whatsapp_number", "user__email")


@admin.register(Turf)
class TurfAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "location", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "location")
